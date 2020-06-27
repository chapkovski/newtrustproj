"""This module is for 'visual' testing - it creates a bunch of data so we can visually
tst the mingler interface.
NOT A PROPER TEST. Proper ones are in test_mingle.py here.
"""
from otree.session import create_session
from trust.models import Player, Decision, Constants, City
from django.db.models import F
import random
from django.conf import settings

drop_out_rate = 0.1


def data_creator(num_participants):
    for i in settings.CITIES:
        City.objects.get_or_create(code=i['code'], defaults={'description': i['name'],
                                                             'eng': i['eng']})

    cities = [(f"{x:02d}") for x in range(1, 13)]
    sessions = []
    for x in cities:
        s = create_session(
            session_config_name='trust_demo_ru',
            num_participants=num_participants,
            label=x,
            modified_session_config_fields=dict(city_code=x)
        )
        sessions.append(s)

    tps = Player.objects.filter(session__in=sessions)
    tps.update(calculable=True)
    tps = Player.objects.filter(session__in=sessions)
    evens = tps.annotate(odd=F('id') % 2).filter(odd=False)
    odds = tps.annotate(odd=F('id') % 2).filter(odd=True)
    odds.update(_role='sender')
    evens.update(_role='receiver')

    # we do this again because update nullifies querysets
    # TODO: It really can be optimized by bulk creation but I am too lazy for that now. Optimize later

    ps = Player.objects.filter(session__in=sessions)
    for p in ps:
        p.create_decisions()
        p.create_beliefs()

    upd_decisions = []
    for d in Decision.objects.filter(decision_type='sender_decision'):
        d.answer = random.choice([0, 10])
        upd_decisions.append(d)
    for d in Decision.objects.filter(decision_type='return_decision'):
        d.answer = random.choice([12, 15, 18])
        upd_decisions.append(d)
    for d in Decision.objects.filter(decision_type='receiver_belief'):
        d.answer = random.choice([0, 10])
        upd_decisions.append(d)
    for d in Decision.objects.filter(decision_type='sender_belief'):
        d.answer = random.choice([12, 15, 18, 21])
        upd_decisions.append(d)
    Decision.objects.bulk_update(upd_decisions, ['answer'])
    # finally let take some of them out by setting calculable to false
    ps = Player.objects.filter(session__in=sessions, calculable=True)
    ids = list(ps.values_list('id', flat=True))

    drop_out_n = int(len(ps) * drop_out_rate)
    drop_out_ids = random.sample(ids, drop_out_n)
    ps.filter(id__in=drop_out_ids).update(calculable=False)
