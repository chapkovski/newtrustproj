"""
Contains models for mingling sessions into larger megasessions, plus some 1to1 to Participant model
"""
from otree.models import Participant, Session
from django.db import models
import random
from trust.models import Constants, City, Player
from otree.api import models as omodels
import pandas as pd
from django.db.models.functions import Abs, Cast
from django.db.models import (Count, F, Q, Max, Sum, Value, IntegerField, Case,
                              When, OuterRef, Subquery, BooleanField, Avg, FloatField )
from django.utils.safestring import mark_safe
import time
from django.urls import reverse


class NotEnoughParticipants(ValueError):
    pass


class TrackerModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MingleSession(TrackerModel):
    """1to1 to prevent double mingling. This is basically the linkage between otree sessions and megasessions"""
    owner = models.OneToOneField(to=Session, on_delete=models.CASCADE, related_name='minglesession')
    megasession = models.ForeignKey(to='MegaSession', on_delete=models.SET_NULL, related_name='minglesessions',
                                    null=True, blank=True)
    city = models.ForeignKey(to=City, on_delete=models.CASCADE, )

    def num_calculable(self):
        return self.owner.trust_player.filter(calculable=True).count()


class MegaSession(TrackerModel):
    """Container for all sessions belonging to one mega. It is also container for participants and megagroups."""
    # TODO: add created_at, updated_at fields everywhere

    comment = models.CharField(max_length=1000, null=True, blank=True)
    payoff_calculated = models.BooleanField(default=False)
    groups_formed = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('MegaSessionDetail', args=[self.id])

    def __str__(self):
        return f'Wrapper for {self.minglesessions.all().count()}'

    @property
    def deletable(self):
        if self.payoff_calculated:
            return False
        return True

    def merge_to_groups(self, group_type, data, type_referral):
        if len(data) == 0:
            return
        maxpk = group_type.objects.all().aggregate(mx=Max('pk'))['mx'] or 0
        newgroups = [group_type(megasession=self, pk=maxpk + i + 1) for i in range(len(data))]
        newgroups = group_type.objects.bulk_create(newgroups)

        parts_to_update = []
        for i, (a, b) in enumerate(data):
            g = newgroups[i]
            setattr(a, type_referral, g)
            setattr(b, type_referral, g)
            parts_to_update.extend([a, b, ])

        MegaParticipant.objects.bulk_update(parts_to_update, [type_referral])
        groups = group_type.objects.filter(megasession=self)
        sender = Subquery(MegaParticipant.objects.filter(**{type_referral: OuterRef('pk')},
                                                         owner__trust_player___role='sender').values(
            'id')[:1])
        receiver = Subquery(MegaParticipant.objects.filter(**{type_referral: OuterRef('pk')},
                                                           owner__trust_player___role='receiver').values(
            'id')[:1])
        groups.update(sender=sender, receiver=receiver)

    def form_groups(self):
        """That takes all megaparticipants and create groups from the random pairs of Senders and receivers"""
        # TODO: we will probably block further group recomposition later
        # if self.payoff_calculated:
        #     return
        # We reset all group memberships:
        self.megaparticipants.filter(owner__trust_player__calculable=True).update(group=None, pseudogroup=None)
        self.megagroups.filter(megaparticipants__isnull=True).delete()
        self.pseudogroups.filter(megaparticipants__isnull=True).delete()

        calculable = self.megaparticipants.filter(owner__trust_player__calculable=True)
        receivers = calculable.filter(owner__trust_player___role='receiver')
        senders = calculable.filter(owner__trust_player___role='sender')
        if receivers.count() == 0 or senders.count() == 0:
            raise NotEnoughParticipants
        smallest, largest = sorted([senders, receivers], key=lambda x: x.count())
        largest = list(largest)
        smallest = list(smallest)
        random.shuffle(largest)
        unmatched = largest[len(smallest):]
        partners_for_unmatched = random.sample(smallest, len(unmatched))
        pairs = list(zip(smallest, largest[:len(smallest)]))
        self.merge_to_groups(group_type=MegaGroup, data=pairs, type_referral='group')
        # Dealing with unmatched
        unmatched_pairs = list(zip(unmatched, partners_for_unmatched))
        self.merge_to_groups(group_type=PseudoGroup, data=unmatched_pairs, type_referral='pseudogroup')
        self.groups_formed = True
        self.save()

    def set_group_data(self, group_type):
        m = group_type.objects.filter(megasession=self)
        # WE GET AND ASSIGN SENDER DESIONS TO GROUP OBJECTS HERE
        subquery_head = group_type.objects.filter(
            id=OuterRef('id')
        ).annotate(sender_city=F('sender__city'),
                   receiver_city=F('receiver__city'))

        sender_decision = Subquery(
            subquery_head.annotate(sender_decision=Sum('sender__owner__trust_player__decisions__answer',
                                                       filter=(Q(
                                                           sender__owner__trust_player__decisions__decision_type='sender_decision'
                                                       ) & Q(
                                                           sender__owner__trust_player__decisions__city=F(
                                                               'receiver_city')
                                                       )))).values('sender_decision')[:1]
        )

        receiver_decision = Subquery(
            subquery_head.annotate(receiver_decision=Sum('receiver__owner__trust_player__decisions__answer',
                                                         filter=(Q(
                                                             receiver__owner__trust_player__decisions__decision_type='return_decision'
                                                         ) & Q(
                                                             receiver__owner__trust_player__decisions__city=F(
                                                                 'sender__city')
                                                         )))).values('receiver_decision')[:1]
        )

        sender_belief_re_receiver = Subquery(
            subquery_head.annotate(sender_belief=Sum('sender__owner__trust_player__decisions__answer',
                                                     filter=(Q(
                                                         sender__owner__trust_player__decisions__decision_type='sender_belief'
                                                     ) & Q(
                                                         sender__owner__trust_player__decisions__city=F(
                                                             'receiver__city')
                                                     )))).values('sender_belief')[:1]
        )
        receiver_belief_re_sender = Subquery(
            subquery_head.annotate(receiver_belief=Sum('receiver__owner__trust_player__decisions__answer',
                                                       filter=(Q(
                                                           receiver__owner__trust_player__decisions__decision_type='receiver_belief'
                                                       ) & Q(
                                                           receiver__owner__trust_player__decisions__city=F(
                                                               'sender__city')
                                                       )))).values('receiver_belief')[:1]
        )

        m.update(sender_decision_re_receiver=sender_decision,
                 receiver_decision_re_sender=receiver_decision,
                 sender_belief_re_receiver=sender_belief_re_receiver,
                 receiver_belief_re_sender=receiver_belief_re_sender,

                 )
        m = group_type.objects.filter(megasession=self)
        receiver_correct_guess = Case(
            When(sender_decision_re_receiver=receiver_belief_re_sender, then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        )
        m.update(sender_belief_diff=Abs(F('receiver_decision_re_sender') - F('sender_belief_re_receiver')), )
        m = group_type.objects.filter(megasession=self)
        m.update(
            has_sender_sent=Case(When(~Q(sender_decision_re_receiver=0), then=Value(True)),
                                 default=Value(False),
                                 output_field=BooleanField()),
            receiver_correct_guess=receiver_correct_guess,
            sender_guess_payoff=Case(
                When(sender_belief_diff=0, then=Value(20)),
                When(sender_belief_diff=3, then=Value(10), ),
                default=Value(0),
                output_field=IntegerField()
            )
        )

    def set_players_payoffs(self, pseudo, ):
        """
             Sender payoff stage 1:
             endowment - amount sent + amount returned
             Sender State 2 payoff:
             exact match from receiver decision: 20 points. 3 points deviation - 10 poins. More 0
             Receiver stage 1 payoff:
             endowment + amount_send * coef - amount_returned
             Receiver stage 2 payoff:
             receiver_belief_bonus (10) for guessing correclty.

             """
        if pseudo:
            condition = {'participant__megaparticipant__group__isnull': True,
                         'participant__megaparticipant__pseudogroup__isnull': False, }
            type_referral = 'pseudogroup'

        else:
            condition = {'participant__megaparticipant__group__isnull': False, }
            type_referral = 'group'
        sender_type_referral = f'sender_{type_referral}'
        receiver_type_referral = f'receiver_{type_referral}'
        players = Player.objects.filter(**condition, participant__megaparticipant__megasession=self)

        sender_players = players.filter(
            participant__megaparticipant=F(f'participant__megaparticipant__{sender_type_referral}__sender'),
        )
        receiver_players = players.filter(
            participant__megaparticipant=F(f'participant__megaparticipant__{receiver_type_referral}__receiver'),
        )

        def group_retrieval_sq(field_name):
            """Returns subquery for updating payoffs"""
            return Subquery(Player.objects.filter(pk=OuterRef('pk')).values(
                f'participant__megaparticipant__{type_referral}__{field_name}')[:1])

        # TODO: if later (when??) we decide to change endowment to something else, that may create problems

        sender_decision = group_retrieval_sq('sender_decision_re_receiver')
        has_sender_sent = Cast(group_retrieval_sq('has_sender_sent'), output_field=IntegerField())
        receiver_decision = group_retrieval_sq('receiver_decision_re_sender')
        receiver_correct_guess = Cast(group_retrieval_sq('receiver_correct_guess'), output_field=IntegerField())
        sender_guess_payoff = group_retrieval_sq('sender_guess_payoff')
        sender_stage1_payoff = Constants.endowment + (receiver_decision - sender_decision) * has_sender_sent
        receiver_stage1_payoff = Constants.endowment + (
                sender_decision * Constants.coef - receiver_decision) * has_sender_sent
        sender_stage2_payoff = sender_guess_payoff
        receiver_stage2_payoff = receiver_correct_guess * Constants.receiver_belief_bonus

        sender_payoff = sender_stage1_payoff + sender_stage2_payoff
        receiver_payoff = receiver_stage1_payoff + receiver_stage2_payoff

        sender_players.update(stage1payoff=sender_stage1_payoff,
                              stage2payoff=sender_stage2_payoff,
                              _payoff=sender_payoff)

        receiver_players.update(stage1payoff=receiver_stage1_payoff,
                                stage2payoff=receiver_stage2_payoff,
                                _payoff=receiver_payoff)

    def calculate_payoffs(self):
        """
        We first set group data (for real and pseudogroups. Then we update players payoffs based on group data.
        Those players who are matched both into a group and pseudogroup are updated only based on their real group data.
        """
        self.set_group_data(group_type=MegaGroup)
        self.set_group_data(group_type=PseudoGroup)
        self.set_players_payoffs(pseudo=False)
        self.set_players_payoffs(pseudo=True)
        # and finally we update all megaparticipants property of payoff_calculated:
        ps = Participant.objects. \
            filter(megaparticipant__megasession=self). \
            update(payoff=Subquery(Participant.objects.filter(pk=OuterRef('pk')).values(
            'trust_player___payoff')[:1]))

        self.megaparticipants.all().update(payoff_calculated=True)
        self.payoff_calculated = True
        self.save()

    def general_stats(self):
        """Return general stats about number of participants"""
        q = self.megaparticipants.filter(owner__trust_player__calculable=True).values(
            city1=F('city__eng'),
            role=F('owner__trust_player___role'),
        ).annotate(
            number=Count('pk')
        ).order_by('city1')
        df = pd.DataFrame(q)
        table = pd.pivot_table(df, values='number', index=['city1'],
                               columns=['role'], fill_value=0)
        return mark_safe(
            table.to_html(classes=['table', 'table-hover', 'table-striped', ]))

    def get_summary_table(self):
        """We get the balance here:
        1. how many participants have been matched with the same city
        2. what an average share of each city per city
        3. what is a standard dev of p.2
        4. NxN table of city shares
        solution is THANKS TO Willem Van Olsem:
        https://stackoverflow.com/questions/62490065/how-to-calculate-frequency-of-pairs-in-queryset/62490197?noredirect=1#comment110523467_62490197
        """

        data = self.megaparticipants.filter(group__isnull=False).filter(
            Q(group__megaparticipants__lt=F('pk')) | Q(group__megaparticipants__gt=F('pk'))
        ).values(
            city1=F('city__description'),
            city2=F('group__megaparticipants__city__eng')
        ).annotate(
            number=Count('pk')
        ).order_by('city1', 'city2')

        df = pd.DataFrame(data)
        df['sumcity'] = df.groupby('city1')['number'].transform('sum')
        df['perc'] = df['number'] / df['sumcity']

        pd.options.display.float_format = '{0:.0%}'.format
        table = pd.pivot_table(df, values='perc', index=['city1'],
                               columns=['city2'], fill_value=0)
        return mark_safe(
            table.to_html(classes=['table', 'table-hover', 'table-striped', 'table-sm', 'table-responsive']))

    def total_payoff(self):
        try:
            single_session = self.megaparticipants.first().owner.session
            exchange_rate = single_session.config.get('real_world_currency_per_point', 1)
            total_p = Participant.objects.filter(megaparticipant__megasession=self).aggregate(Sum('payoff'))[
                'payoff__sum']
            return total_p, float(total_p * exchange_rate)
        except (Participant.DoesNotExist, MegaParticipant.DoesNotExist):
            pass

    def payoff_stats(self):
        parts = self.megaparticipants.annotate(role=F('owner__trust_player___role'),
                                               payoff=F('owner__payoff'),).\
            values('role','city__eng', ).annotate(avpayoff=Cast(Avg('payoff'), output_field=FloatField())).order_by('role')
        df = pd.DataFrame(parts)
        pd.reset_option('float_format')

        table = pd.pivot_table(df, values='avpayoff', index=['city__eng'],
                               columns=['role'], fill_value=0)

        return mark_safe(
            table.to_html(classes=['table', 'table-hover', 'table-striped', ]))



class MegaParticipant(TrackerModel):
    type_correspondence = dict(
        sender=dict(decision='sender_decision_re_receiver',
                    belief='sender_belief_re_receiver'),
        receiver=dict(decision='receiver_decision_re_sender',
                      belief='receiver_belief_re_sender'),
    )
    """1to1 link to participant for freezing those whose payoffs were calculated.
    Not really necessary but maybe convenient for future extensions, since we can't interfere to Participant model"""
    owner = models.OneToOneField(to=Participant, on_delete=models.CASCADE, )
    city = models.ForeignKey(to=City, on_delete=models.CASCADE, )
    payoff_calculated = omodels.BooleanField(blank=True, initial=False)
    megasession = models.ForeignKey(to='MegaSession', on_delete=models.CASCADE, related_name='megaparticipants')
    group = models.ForeignKey(to='MegaGroup',
                              on_delete=models.SET_NULL,
                              related_name='megaparticipants',
                              null=True,
                              blank=True)

    pseudogroup = models.ForeignKey(to='PseudoGroup',
                                    on_delete=models.SET_NULL,
                                    related_name='megaparticipants',
                                    null=True,
                                    blank=True)

    def __str__(self):
        return f'Megaparticipant {self.owner.code}'

    def get_absolute_url(self):
        return reverse('mega_participant_results', kwargs={'code': self.owner.code})

    @property
    def player(self):
        return self.owner.trust_player.first()

    @property
    def role(self):
        """just for template rendering"""
        return self.player._role

    def _retrieval(self, group_type, field_type):
        g = getattr(self, group_type)
        field_name = self.type_correspondence[self.role][field_type]
        return getattr(g, field_name)

    def decision(self, pseudo):
        if pseudo and self.pseudogroup:
            return self._retrieval('pseudogroup', 'decision')
        else:
            return self._retrieval('group', 'decision')

    def belief(self, pseudo):
        if pseudo and self.pseudogroup:
            return self._retrieval('pseudogroup', 'belief')
        else:
            return self._retrieval('group', 'belief')

    @property
    def other(self):
        if self.group:
            return self.group.megaparticipants.get(~Q(id=self.id))
        if self.pseudogroup:
            return self.pseudogroup.megaparticipants.get(~Q(id=self.id))


class GeneralGroup(TrackerModel):
    class Meta:
        abstract = True

    sender_decision_re_receiver = omodels.IntegerField(blank=True)
    has_sender_sent = omodels.BooleanField(blank=True)
    receiver_decision_re_sender = omodels.IntegerField(blank=True)
    sender_belief_re_receiver = omodels.IntegerField(blank=True)
    receiver_belief_re_sender = omodels.IntegerField(blank=True)
    receiver_correct_guess = omodels.BooleanField(blank=True)
    sender_belief_diff = omodels.IntegerField(blank=True)
    sender_guess_payoff = omodels.IntegerField(blank=True)

    def get_player_by_role(self, role):
        for p in self.megaparticipants.all():
            if p.player._role == role:
                return p.player


class MegaGroup(GeneralGroup):
    """links two random participants together to calculate their payoffs.
    Will it contain the code for actual payoff calculations? Seems logical place for that.
    Megagroup is different from a normal oTree group, because the participants can belong to the different oTree sessions,
    the umbrella is megasession."""
    megasession = models.ForeignKey(to='MegaSession', on_delete=models.CASCADE, related_name='megagroups')
    sender = models.OneToOneField(to=MegaParticipant, on_delete=models.CASCADE,
                                  related_name='sender_group', null=True, blank=True)
    receiver = models.OneToOneField(to=MegaParticipant, on_delete=models.CASCADE,
                                    related_name='receiver_group', null=True, blank=True)


class PseudoGroup(GeneralGroup):
    """
    A wrapper to store unmatched participants with their counterparts.
    A few notes on what is going on with unmatched participants:
    First we get all receivers, all senders, and match them. The difference abs(R-S) remain unmatched. Then
    we pick len(R-S) from matched (from the role that is shortest). and match them into Pseudogroups with unmatched.
    Thus in each pseudogroup there is matched and unmatched participant.
    When we calculate payoffs for each group member in PseudoGroup, we update the payoffs of unmatched, because
    matched participants get their payoffs from their real (Mega) group.
    """
    megasession = models.ForeignKey(to='MegaSession', on_delete=models.CASCADE, related_name='pseudogroups')
    sender = models.OneToOneField(to=MegaParticipant, on_delete=models.CASCADE,
                                  related_name='sender_pseudogroup', null=True, blank=True)
    receiver = models.OneToOneField(to=MegaParticipant, on_delete=models.CASCADE,
                                    related_name='receiver_pseudogroup', null=True, blank=True)
