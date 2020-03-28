from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
from .cq_models import CQPlayer
from django.db import models as djmodels
from django.conf import settings
import random
import json
from django.core.serializers import serialize
from otree.models import Session
from django_pandas.managers import DataFrameManager

author = 'Philipp Chapkovski'

doc = """
Interregional trust game. 
"""


class Constants(BaseConstants):
    name_in_url = 'trust'
    players_per_group = None
    num_rounds = 1
    endowment = 10
    step = 3
    coef = 3
    max_return = endowment * coef
    sender_choices = ((endowment, "Да"), (0, 'Нет'))
    receiver_choices = list(range(0, endowment * coef + 1, step))
    expanded_receiver_choices = list(zip(receiver_choices, receiver_choices))
    receiver_belief_bonus = 10
    sender_belief_bonuses = {0: 20, 3: 10}
    roles = {'Sender': 'А', 'Receiver': 'Б'}
    blocked_page_names = ['IntroStage1',
                          'IntroStage2',
                          ]


def return_choices():
    return list(range(0, Constants.endowment + 1, Constants.step))


class City(djmodels.Model):
    code = models.StringField(unique=True)
    description = models.StringField(unique=True)

    def __str__(self):
        return f'Code: {self.code}; Description: {self.description}'


from json import JSONEncoder


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class Subsession(BaseSubsession):
    matched_different = models.BooleanField(default=True)
    session_config_dump = models.LongStringField()

    def vars_for_admin_report(self):
        blockers = Blocker.objects.filter(session=self.session).order_by('pk')
        r = dict(blockers=blockers)
        if self.session.vars.get('monitor_cubicles'):
            try:
                city1 = City.objects.get(code=self.session.config.get('city1'))
                city2 = City.objects.get(code=self.session.config.get('city2'))
                city1_players = [p for p in self.session.get_participants() if p.vars.get('city') == city1.code]
                city2_players = [p for p in self.session.get_participants() if p.vars.get('city') == city2.code]
                city1_busy_cubicles = [p.vars.get('pc_id') for p in city1_players if p.vars.get('pc_id')]
                city2_busy_cubicles = [p.vars.get('pc_id') for p in city2_players if p.vars.get('pc_id')]
                potential_cubicles_city1 = list(range(1, self.session.config.get('num_cubicles_city_1') + 1))
                potential_cubicles_city2 = list(range(1, self.session.config.get('num_cubicles_city_2') + 1))
                city1_free_cubicles = list(set(potential_cubicles_city1).difference(set(city1_busy_cubicles)))
                city2_free_cubicles = list(set(potential_cubicles_city2).difference(set(city2_busy_cubicles)))

                cubicle_data = dict(
                    busy_cubicles=dict(city1=city1_busy_cubicles, city2=city2_busy_cubicles),
                    free_cubicles=dict(city1=city1_free_cubicles, city2=city2_free_cubicles),
                    city1=city1,
                    city2=city2,
                )
                r = {**r, 'cubicle_data': cubicle_data}
            except:  # bad idea but we just need to be 100% sure that it won't block the admin page under no circumstances
                pass
        return r

    @property
    def cities(self):
        return [self.session.config.get('city1'), self.session.config.get('city2')]

    def creating_session(self):
        from .pages import page_sequence
        if not self.session.config.get('debug'):
            active_blockers = [p.__name__ for p in page_sequence if getattr(p, 'lockable', False)]
            blockers = [Blocker(page=i, session=self.session, locked=True) for i in active_blockers]
            Blocker.objects.bulk_create(blockers)
        self.session_config_dump = json.dumps(self.session.config, cls=MyEncoder)

        ########### BLOCK: monitor cubicles ##############################################################
        # some sanity check to guarantee non crushing monitor
        ncub1 = self.session.config.get('num_cubicles_city_1')
        ncub2 = self.session.config.get('num_cubicles_city_2')
        if isinstance(ncub1, int) and isinstance(ncub1, int) and ncub1 + ncub2 < 100:
            self.session.vars['monitor_cubicles'] = True
        ############ END OF: monitor cubicles #############################################################

        for p in self.get_players():
            p.participant.vars['city_order'] = random.choice([True, False])
            p.city_order = p.participant.vars['city_order']
        if self.session.num_participants % 2 != 0:
            raise Exception('Number of participants should be even!')
        for i in settings.CITIES:
            City.objects.get_or_create(code=i['code'], defaults={'description': i['name']})
        registered_cities = set(City.objects.all().values_list('code', flat=True))
        if not set(self.cities).issubset(registered_cities):
            raise Exception('Вы ввели неверный код для одного из городов!')
        if len(self.cities) != len(set(self.cities)):
            raise Exception('Вы ввели два одинаковых города! Не надо так.')


class Group(BaseGroup):
    sender_decision_re_receiver = models.IntegerField()
    receiver_decision_re_sender = models.IntegerField()
    sender_belief_re_receiver = models.IntegerField()

    receiver_belief_re_receiver = models.IntegerField()
    receiver_correct_guess = models.BooleanField()
    sender_belief_diff = models.IntegerField()
    # group of dumping vars
    sender_decisions_dump = models.LongStringField()
    receiver_decisions_dump = models.LongStringField()
    sender_beliefs_dump = models.LongStringField()
    receiver_beliefs_dump = models.LongStringField()

    def set_payoffs(self):
        sender = self.get_player_by_role('Sender')
        receiver = self.get_player_by_role('Receiver')
        sender_city = sender.get_city_obj()
        receiver_city = receiver.get_city_obj()

        def stage1_payoffs():
            self.sender_decision_re_receiver = sender.senderdecisions.get(city=receiver_city).answer
            has_sender_sent = self.sender_decision_re_receiver != 0
            self.receiver_decision_re_sender = receiver.returndecisions.get(city=sender_city).answer
            sender.stage1payoff = sender.endowment + (
                    self.receiver_decision_re_sender - self.sender_decision_re_receiver) * has_sender_sent

            receiver.stage1payoff = receiver.endowment + (
                    self.sender_decision_re_receiver * Constants.coef - self.receiver_decision_re_sender) * has_sender_sent

        def stage2_payoffs():
            self.sender_belief_re_receiver = sender.senderbeliefs.get(city=receiver_city).answer
            self.receiver_belief_re_receiver = receiver.returnerbeliefs.get(city=sender_city).answer
            self.receiver_correct_guess = self.receiver_belief_re_receiver == self.sender_decision_re_receiver
            receiver.stage2payoff = self.receiver_correct_guess * Constants.receiver_belief_bonus
            self.sender_belief_diff = abs(self.receiver_decision_re_sender - self.sender_belief_re_receiver)
            sender.stage2payoff = Constants.sender_belief_bonuses.get(self.sender_belief_diff) or 0

        stage1_payoffs()
        stage2_payoffs()
        self.dump_extra()
        for p in self.get_players():
            p.payoff = p.stage1payoff + p.stage2payoff
            p.dump_vars()

    def dump_extra(self):
        sender = self.get_player_by_role('Sender')
        receiver = self.get_player_by_role('Receiver')
        self.sender_decisions_dump = serialize('json', sender.senderdecisions.all())
        self.receiver_decisions_dump = serialize('json', receiver.returndecisions.all())
        self.sender_beliefs_dump = serialize('json', sender.senderbeliefs.all())
        self.receiver_beliefs_dump = serialize('json', receiver.returnerbeliefs.all())
        for p in self.get_players():
            p.average_beliefs_on_send_dump = serialize('json', p.averageonsendbeliefs.all())
            p.average_beliefs_on_return_dump = serialize('json', p.averageonreturnbeliefs.all())
            p.participant_vars_dump = json.dumps(p.participant.vars, cls=MyEncoder)


class Player(CQPlayer):
    endowment = models.CurrencyField(initial=Constants.endowment)
    city = models.StringField()
    partner_city = models.StringField()
    _role = models.StringField()
    stage1payoff = models.CurrencyField(initial=0)
    stage2payoff = models.CurrencyField(initial=0)
    city_order = models.BooleanField()
    average_beliefs_on_send_dump = models.LongStringField()
    average_beliefs_on_return_dump = models.LongStringField()
    participant_vars_dump = models.LongStringField()

    @property
    def role_desc(self):
        return Constants.roles.get(self.role())

    def get_city_obj(self):
        return City.objects.get(code=self.city)

    @property
    def guess(self):
        if self.role() == 'Sender':
            return self.senderbeliefs.get(city=self.other.get_city_obj()).answer
        else:
            return self.returnerbeliefs.get(city=self.other.get_city_obj()).answer

    @property
    def guess_desc(self):
        if self.role() == 'Sender':
            return c(self.guess)
        else:
            return 'не передать свою начальную сумму' if self.guess == 0 else 'передать свою начальную сумму'

    @property
    def decision(self):
        if self.role() == 'Sender':
            return self.senderdecisions.get(city=self.other.get_city_obj()).answer
        else:
            return self.returndecisions.get(city=self.other.get_city_obj()).answer

    @property
    def decision_desc(self):
        if self.role() == 'Sender':
            return 'не передать свою начальную сумму' if self.decision == 0 else 'передать свою начальную сумму'
        else:
            return f'вернуть {c(self.decision)}'

    def dump_vars(self):
        dump = dict(
            city=self.get_city_obj().description,
            guess=self.guess_desc,
            other_role_desc=self.other.role_desc,
            own_decision=self.decision_desc,
            partner_city=self.other.get_city_obj().description,
            partner_decision=self.other.decision_desc,
            role=self.role(),
            role_desc=self.role_desc,
            sender_decision=self.group.sender_decision_re_receiver != 0,
            stage1payoff=self.stage1payoff,
            stage2payoff=self.stage2payoff,
            stage1payoff_rubles=c(self.stage1payoff).to_real_world_currency(self.session),
            stage2payoff_rubles=c(self.stage2payoff).to_real_world_currency(self.session),
        )
        self.participant.vars = {**self.participant.vars, **dump}

    @property
    def other(self):
        return self.get_others_in_group()[0]

    def role(self):
        return self._role

    def create_decisions(self):
        if self.role() == 'Sender':
            self.create_sender_decisions()
        else:
            self.create_receiver_decisions()

    def create_beliefs(self):
        if self.role() == 'Sender':
            self.create_sender_beliefs()
        else:
            self.create_receiver_beliefs()

    def create_averages(self):
        self.create_sender_averages()
        self.create_receiver_averages()

    def create_sender_averages(self):
        self._universal_creator('average_on_return_belief')

    def create_receiver_averages(self):
        self._universal_creator('average_on_send_belief')

    def create_sender_decisions(self):
        self._universal_creator('sender_decision')

    def create_receiver_decisions(self):
        self._universal_creator('return_decision')

    def create_sender_beliefs(self):
        self._universal_creator('sender_belief')

    def create_receiver_beliefs(self):
        self._universal_creator('receiver_belief')

    def _universal_creator(self, decision_type):
        # todo: optimize with bulk_create
        for city in City.objects.all():
            Decision.objects.create(city=city, owner=self, decision_type=decision_type)

    def _decision_getter(self, decision_type):
        return self.decisions.filter(decision_type=decision_type)

    @property
    def senderdecisions(self):
        return self._decision_getter('sender_decision')

    @property
    def returndecisions(self):
        return self._decision_getter('return_decision')

    @property
    def senderbeliefs(self):
        return self._decision_getter('sender_belief')

    @property
    def returnerbeliefs(self):
        return self._decision_getter('receiver_belief')

    @property
    def averageonsendbeliefs(self):
        return self._decision_getter('average_on_send_belief')

    @property
    def averageonreturnbeliefs(self):
        return self._decision_getter('average_on_return_belief')


decision_types = ['sender_decision', 'return_decision', 'sender_belief', 'receiver_belief', 'average_on_send_belief',
                  'average_on_return_belief']


class Decision(djmodels.Model):
    city = djmodels.ForeignKey(to=City, on_delete=djmodels.CASCADE, null=True)
    owner = djmodels.ForeignKey(to=Player, on_delete=djmodels.CASCADE, related_name="decisions")
    decision_type = models.StringField(choices=decision_types)
    answer = models.IntegerField()
    forpd = DataFrameManager()
    objects = djmodels.Manager()


class Blocker(djmodels.Model):
    session = djmodels.ForeignKey(to=Session, related_name='blockers', on_delete=djmodels.CASCADE)
    page = models.StringField()
    locked = models.BooleanField(initial=False)
