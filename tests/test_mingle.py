from django.test import TestCase
from mingle.models import MegaSession, MingleSession, MegaParticipant, MegaGroup
from otree.session import create_session
from otree.models import Session, Participant
from trust.models import Player, Decision
from django.db.models import F

class AnimalTestCase(TestCase):
    def setUp(self):
        MegaSession.objects.create(comment="lion")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = MegaSession.objects.get(comment="lion")
        self.assertEqual(lion.speak(), 'comment lion')
        print(f'TOTSESSIONS: {Session.objects.all().count()}')
        cities = [(f"{x:02d}") for x in range(1, 13)]
        sessions = [
            create_session(
                session_config_name='trust_demo_ru',
                num_participants=2,
                modified_session_config_fields=dict(city_code=x)
            ) for x in cities]

        m = MegaSession.objects.create()
        MingleSession.objects.all().update(megasession=m)
        parts = Participant.objects.filter(session__in=sessions)
        megapars = [MegaParticipant(owner=i, megasession=m) for i in parts]
        MegaParticipant.objects.bulk_create(megapars)
        tps = Player.objects.filter(session__in=sessions)
        tps.update(calculable=True)
        tps = Player.objects.filter(session__in=sessions)
        evens = tps.annotate(odd=F('id') % 2).filter(odd=False)
        odds = tps.annotate(odd=F('id') % 2).filter(odd=True)
        odds.update(_role='sender')
        evens.update(_role='receiver')
        print(MegaParticipant.objects.all().count())

        m.form_groups()
        senders = Player.objects.filter(_role='sender')
        receivers = Player.objects.filter(_role='receiver')
        ps = Player.objects.filter(session__in=sessions)
        for p in ps:
            p.create_decisions()
            p.create_beliefs()

        Decision.objects.filter(decision_type='sender_decision').update(answer=0)
        Decision.objects.filter(decision_type='return_decision').update(answer=3)
        Decision.objects.filter(decision_type='sender_belief').update(answer=3)
        Decision.objects.filter(decision_type='receiver_belief').update(answer=0)
        for p in Participant.objects.all():
            print("BEFOREBPAYOFF", p.payoff)
        m.calculate_payoffs()
        for p in Participant.objects.all():
            print("AFTERBPAYOFF", p.payoff)

