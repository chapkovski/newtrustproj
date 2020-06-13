"""
Contains models for mingling sessions into larger megasessions, plus some 1to1 to Participant model
"""
from otree.models import Participant, Session
from django.db import models
import random
from trust.models import Constants
from otree.api import models as omodels


class MingleSession(models.Model):
    """1to1 to prevent double mingling. This is basically the linkage between otree sessions and megasessions"""
    owner = models.OneToOneField(to=Session, on_delete=models.CASCADE, related_name='minglesession')
    megasession = models.ForeignKey(to='MegaSession', on_delete=models.SET_NULL, related_name='minglesessions',
                                    null=True, blank=True)


class MegaSession(models.Model):
    """Container for all sessions belonging to one mega. It is also container for participants and megagroups."""
    # TODO: add created_at, updated_at fields everywhere
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=1000, null=True, blank=True)
    payoff_calculated = models.BooleanField(default=False)
    groups_formed = models.BooleanField(default=False)

    def __str__(self):
        return f'Wrapper for {self.minglesessions.all().count()}'

    def form_groups(self):
        """That takes all megaparticipants and create groups from the random pairs of Senders and receivers"""
        if self.payoff_calculated:
            return

        """somewhere here we need to retrieve only those participants who are not dropouts.
        then we need to split them into senders and receivers
        shuffle both sets
        drop the difference between shortest and longests sets to make them equal
        and form groups."""
        calculable = self.megaparticipants.filter(owner__trust_player__calculable=True)
        receivers = calculable.filter(owner__trust_player___role='receiver')
        senders = calculable.filter(owner__trust_player___role='sender')
        if receivers.count() == 0 or senders.count() == 0:
            raise ValueError('NOT ENOUGH PARTICIPANTS')
        smallest, largest = sorted([senders, receivers], key=lambda x: x.count())
        largest = list(largest)
        smallest = list(smallest)
        random.shuffle(largest)
        unmatched = largest[len(smallest):]
        partners_for_unmatched = random.sample(smallest, len(unmatched))
        pairs = zip(smallest, largest[:len(smallest)])
        for g in pairs:
            newg = MegaGroup.objects.create(megasession=self)
            for p in g:
                p.group = newg
                p.save()
        unmatched_pairs = zip(unmatched, partners_for_unmatched)
        for g in unmatched_pairs:
            newg = PseudoGroup.objects.create(megasession=self)
            for p in g:
                p.pseudogroup = newg
                p.save()
        self.groups_formed = True
        self.save()

    def calculate_payoffs(self):
        """loop over all groups and make payoff calculations"""
        if self.payoff_calculated:
            return
        for g in self.megagroups.all():
            g.set_payoffs()
        for g in self.pseudogroups.all():
            g.set_payoffs()
        self.payoff_calculated = True
        self.save()


class MegaParticipant(models.Model):
    """1to1 link to participant for freezing those whose payoffs were calculated.
    Not really necessary but maybe convenient for future extensions, since we can't interfere to Participant model"""
    owner = models.OneToOneField(to=Participant, on_delete=models.CASCADE, )
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

    @property
    def matched(self):
        return self.group is not None

    @property
    def player(self):
        return self.owner.trust_player.first()

    def get_another(self, group):
        return group.megaparticipants.exclude(id=self.id).first()

    def group_partner(self):
        """this one will return partner for those who are matched in groups or groups AND pseudogrups.
        for those who are only in pseudogroups will return their pseudogrup partner.
        """
        if self.group:
            return self.get_another(self.group)
        if self.pseudogroup:
            return self.get_another(self.pseudogroup)

    @property
    def other_city(self):
        return self.group_partner().player.city

    @property
    def guess(self):
        if self.player.role() == 'sender':
            return self.player.senderbeliefs.get(city=self.other_city).answer
        else:
            return self.player.returnerbeliefs.get(city=self.other_city).answer

    @property
    def decision(self):
        if self.player.role() == 'sender':
            return self.player.senderdecisions.get(city=self.other_city).answer
        else:
            return self.player.returndecisions.get(city=self.other_city).answer


class GeneralGroup(models.Model):
    class Meta:
        abstract = True

    sender_decision_re_receiver = omodels.IntegerField()
    receiver_decision_re_sender = omodels.IntegerField()
    sender_belief_re_receiver = omodels.IntegerField()
    receiver_belief_re_receiver = omodels.IntegerField()
    receiver_correct_guess = omodels.BooleanField()
    sender_belief_diff = omodels.IntegerField()

    def get_player_by_role(self, role):
        for p in self.megaparticipants.all():
            if p.player._role == role:
                return p.player

    def get_players_for_payoff(self):
        """by default we only get the participants who are matched, it is overriden in pseudogroup"""
        return [p.player for p in self.megaparticipants.all()]

    def set_payoffs(self) -> None:
        """Get roles, calculate payoffs. It can be done more elegantly, I guess, this one is a bit of a mess,
        but just too tired to figure this out now. The major part of ugliness is because of these fucking
        pseudogrups that we have to take into account - without them it would be much more concise."""
        sender = self.get_player_by_role('sender')
        receiver = self.get_player_by_role('receiver')
        sender_city = sender.get_city_obj()
        receiver_city = receiver.get_city_obj()

        def stage1_calculations():
            """Make ready everything for stage1 payoffs (but does not assign it to users, because
            we don't know if we need to do it for matched/unmatched participants"""
            self.sender_decision_re_receiver = sender.senderdecisions.get(city=receiver_city).answer
            self.receiver_decision_re_sender = receiver.returndecisions.get(city=sender_city).answer

        def stage2_calculations():
            """Make ready everything for stage2 payoffs (but does not assign it to users, because
             we don't know if we need to do it for matched/unmatched participants"""
            self.sender_belief_re_receiver = sender.senderbeliefs.get(city=receiver_city).answer
            self.receiver_belief_re_receiver = receiver.returnerbeliefs.get(city=sender_city).answer
            self.receiver_correct_guess = self.receiver_belief_re_receiver == self.sender_decision_re_receiver

            self.sender_belief_diff = abs(self.receiver_decision_re_sender - self.sender_belief_re_receiver)

        stage1_calculations()
        stage2_calculations()
        self.save()
        """So for real (mega) groups we calculate payoffs for both players. 
        For pseudogroups only for ungrouped ones, and ignore those who are already matched. """
        for p in self.get_players_for_payoff():
            has_sender_sent = self.sender_decision_re_receiver != 0
            if p.role() == 'sender':
                p.stage1payoff = sender.endowment + (
                        self.receiver_decision_re_sender - self.sender_decision_re_receiver) * has_sender_sent
                p.stage2payoff = self.receiver_correct_guess * Constants.receiver_belief_bonus

            else:
                p.stage1payoff = receiver.endowment + (
                        self.sender_decision_re_receiver * Constants.coef - self.receiver_decision_re_sender) * has_sender_sent
                p.stage2payoff = Constants.sender_belief_bonuses.get(self.sender_belief_diff) or 0

            p.payoff = p.stage1payoff + p.stage2payoff
            p.save()


class MegaGroup(GeneralGroup):
    """links two random participants together to calculate their payoffs.
    Will it contain the code for actual payoff calculations? Seems logical place for that.
    Megagroup is different from a normal oTree group, because the participants can belong to the different oTree sessions,
    the umbrella is megasession."""
    megasession = models.ForeignKey(to='MegaSession', on_delete=models.CASCADE, related_name='megagroups')


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

    def get_players_for_payoff(self):
        """We override this in order not to touch the matched players"""
        return [p.player for p in self.megaparticipants.all() if not p.matched]
