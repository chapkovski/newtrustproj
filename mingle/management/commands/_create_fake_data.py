"""This module is for 'visual' testing - it creates a bunch of data so we can visually
tst the mingler interface.
NOT A PROPER TEST. Proper ones are in test_mingle.py here.
"""
from otree.session import create_session
from trust.models import Player, Decision, Constants, City
from django.db.models import F
from mingle.utils import  time_check
import random
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

drop_out_rate = 0.1

@time_check
def generate_rest(sessions, upd_decisions):
    Decision.objects.bulk_update(upd_decisions, ['answer'])
    # finally let take some of them out by setting calculable to false
    ps = Player.objects.filter(session__in=sessions, calculable=True)
    ids = list(ps.values_list('id', flat=True))

    drop_out_n = int(len(ps) * drop_out_rate)
    drop_out_ids = random.sample(ids, drop_out_n)
    ps.filter(id__in=drop_out_ids).update(calculable=False)

def data_creator(num_participants):
    for i in settings.CITIES:
        City.objects.get_or_create(code=i['code'], defaults={'description': i['name'],
                                                             'eng': i['eng']})

    cities = [(f"{x:02d}") for x in range(1, 13)]
    sessions = []
    for x in cities:
        logger.info(f'Creating session for city: {x}; participants:{num_participants} ')
        s = create_session(
            session_config_name='trust_ru',
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

    upd_decisions = []
    ds = Decision.objects.filter(owner__session__in=sessions)
    for d in ds.filter(decision_type='sender_decision', owner___role='sender'):
        d.answer = random.choice([0, 10])
        upd_decisions.append(d)
    for d in ds.filter(decision_type='return_decision', owner___role='receiver'):
        d.answer = random.choice([12, 15, 18])
        upd_decisions.append(d)
    for d in ds.filter(decision_type='receiver_belief', owner___role='receiver'):
        d.answer = random.choice([0, 10])
        upd_decisions.append(d)
    for d in ds.filter(decision_type='sender_belief', owner___role='sender'):
        d.answer = random.choice([12, 15, 18, 21])
        upd_decisions.append(d)


    generate_rest(sessions, upd_decisions)
