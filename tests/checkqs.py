"""
testing how the group info retrieval works

"""

from trust.models import Player, Constants
from mingle.models import  MegaSession, MegaGroup

import time

start = time.time()
from django.db import connection, reset_queries

reset_queries()
print('FFFBEGIN', len(connection.queries))
from django.db.models import (Count, F, Func, Q, Max, Sum, Value, IntegerField, CharField, ExpressionWrapper, Min, Case, \
                              When, OuterRef, Subquery, BooleanField)

# We begin function to calculate payoffs somewhere here (with obtaining megasession id)

m = MegaGroup.objects.filter(megasession__id=4)
# WE GET AND ASSIGN SENDER DESIONS TO GROUP OBJECTS HERE
subquery_head = MegaGroup.objects.filter(
    id=OuterRef('id')
).annotate(sender_city=F('sender__city'),
           receiver_city=F('receiver__city'))

sender_decision = Subquery(
    subquery_head.annotate(sender_decision=Sum('sender__owner__trust_player__decisions__answer',
                                               filter=(Q(
                                                   sender__owner__trust_player__decisions__decision_type='sender_decision'
                                               ) & Q(
                                                   sender__owner__trust_player__decisions__city=F('receiver_city')
                                               )))).values('sender_decision')[:1]
)

receiver_decision = Subquery(
    subquery_head.annotate(receiver_decision=Sum('receiver__owner__trust_player__decisions__answer',
                                                 filter=(Q(
                                                     receiver__owner__trust_player__decisions__decision_type='return_decision'
                                                 ) & Q(
                                                     receiver__owner__trust_player__decisions__city=F('sender__city')
                                                 )))).values('receiver_decision')[:1]
)

sender_belief_re_receiver = Subquery(
    subquery_head.annotate(sender_belief=Sum('sender__owner__trust_player__decisions__answer',
                                             filter=(Q(
                                                 sender__owner__trust_player__decisions__decision_type='sender_belief'
                                             ) & Q(
                                                 sender__owner__trust_player__decisions__city=F('receiver__city')
                                             )))).values('sender_belief')[:1]
)
receiver_belief_re_sender = Subquery(
    subquery_head.annotate(receiver_belief=Sum('receiver__owner__trust_player__decisions__answer',
                                               filter=(Q(
                                                   receiver__owner__trust_player__decisions__decision_type='receiver_belief'
                                               ) & Q(
                                                   receiver__owner__trust_player__decisions__city=F('sender__city')
                                               )))).values('receiver_belief')[:1]
)

m = m.update(sender_decision_re_receiver=sender_decision,
             receiver_decision_re_sender=receiver_decision,
             sender_belief_re_receiver=sender_belief_re_receiver,
             receiver_belief_re_sender=receiver_belief_re_sender,
             )
m = MegaGroup.objects.filter(megasession__id=4)

receiver_correct_guess = Case(
    When(sender_decision_re_receiver=receiver_belief_re_sender, then=Value(True)),
    default=Value(False),
    output_field=BooleanField(),
)

m = m.update(
    receiver_correct_guess=receiver_correct_guess,
    sender_belief_diff=F('receiver_decision_re_sender') - F('sender_belief_re_receiver'),
    sender_guess_payoff=Case(
        When(sender_belief_diff=0, then=Value(20)),
        When(sender_belief_diff=3, then=Value(10), ),
        default=Value(0),
        output_field=IntegerField()
    )
)

m = MegaSession.objects.get(id=4)
players = Player.objects.filter(participant__megaparticipant__megasession=m)
sender_players = players.filter(
    participant__megaparticipant=F('participant__megaparticipant__sender_group__sender'),
)
receiver_players = players.filter(
    participant__megaparticipant=F('participant__megaparticipant__receiver_group__receiver'),
)

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


def group_retrieval_sq(field_name):
    """Returns subquery for updating payoffs"""
    # TODO: REMOVE TWO LINES IN PROD:
    from trust.models import Player, Decision, Constants
    from django.db.models import (OuterRef, Subquery)
    return Subquery(Player.objects.filter(pk=OuterRef('pk')).values(
        f'participant__megaparticipant__group__{field_name}')[:1])


from django.db.models.functions import Abs

# TODO: if later (when??) we decide to change endowment to something else, that may create problems

sender_decision = group_retrieval_sq('sender_decision_re_receiver')
receiver_decision = group_retrieval_sq('receiver_decision_re_sender')
sender_belief = group_retrieval_sq('sender_belief_re_receiver')
receiver_belief = group_retrieval_sq('receiver_belief_re_sender')
receiver_correct_guess = group_retrieval_sq('receiver_correct_guess')
sender_guess_payoff = group_retrieval_sq('sender_guess_payoff')

sender_stage1_payoff = Constants.endowment - sender_decision + receiver_decision
receiver_stage1_payoff = Constants.endowment + sender_decision * Constants.coef - receiver_decision
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

print(f'FFF:{len(connection.queries)}')
end = time.time()
print(end - start)
