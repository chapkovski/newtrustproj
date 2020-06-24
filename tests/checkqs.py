"""
testing how the group info retrieval works

"""
from otree.session import create_session
from trust.models import Player, Decision, Constants
from mingle.models import MegaParticipant, MegaSession, MegaGroup
import random
import pandas as pd
import numpy as np
import time

start = time.time()
from django.db import connection, reset_queries
reset_queries()
print('FFFBEGIN',len(connection.queries))
from django.db.models import Count, F, Func, Q, Max, Sum, Value, IntegerField, CharField, ExpressionWrapper, Min, Case, \
    When, OuterRef, Subquery

# g = MegaGroup.objects.get(id=1)
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
receiver_belief_re_receiver = Subquery(
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
             receiver_belief_re_receiver=receiver_belief_re_receiver
             )
# m = m.update(receiver_decision_re_sender=receiver_decision)
# for i in m:
#     print(i.sender_decision)
print(f'FFF:{len(connection.queries)}')
end = time.time()
print(end - start)