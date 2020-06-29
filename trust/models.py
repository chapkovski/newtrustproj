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
from mingle.utils import time_check
from django_pandas.managers import DataFrameManager
from django.utils.translation import gettext_lazy as _

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
    sender_choices = ((endowment, _("Да")), (0, _('Нет')))
    receiver_choices = list(range(0, endowment * coef + 1, step))
    expanded_receiver_choices = list(zip(receiver_choices, receiver_choices))
    receiver_belief_bonus = 10
    sender_belief_bonuses = {0: 20, 3: 10}
    roles = {'sender': 'А', 'receiver': 'Б'}

    cities = settings.CITIES
    GOOGLE_API_KEY = settings.GOOGLE_API_KEY


def return_choices():
    return list(range(0, Constants.endowment + 1, Constants.step))


class City(djmodels.Model):
    code = models.StringField(unique=True)
    description = models.StringField(unique=True)
    eng = models.StringField()

    def __str__(self):
        return f'Code: {self.code}; Name: {self.eng}'


from json import JSONEncoder


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class Subsession(BaseSubsession):
    session_config_dump = models.LongStringField()

    def creating_session(self):
        self.session_config_dump = json.dumps(self.session.config, cls=MyEncoder)
        if self.session.num_participants % 2 != 0:
            raise Exception('Number of participants should be even!')
        for i in settings.CITIES:
            City.objects.get_or_create(code=i['code'], defaults={'description': i['name'],
                                                                 'eng': i['eng']})
        cur_city = self.session.config.get('city_code')
        city_in = City.objects.filter(code=cur_city)
        if not city_in.exists():
            raise Exception(_('Вы ввели неверный код для одного из городов!'))
        """We get the city and assign its objects to all players"""
        for p in self.get_players():
            p.city = city_in.first()
        # TODO: add requirements to plug toloka pool and project ids
        # toloka_project_id
        # toloka_pool_id


class Group(BaseGroup):
    def set_players_params(self):
        for p in self.get_players():
            p.set_params()


class Player(CQPlayer):
    endowment = models.CurrencyField(initial=Constants.endowment)
    city = djmodels.ForeignKey(to='City', related_name='players', null=True, blank=True, on_delete=djmodels.SET_NULL)
    _role = models.StringField()
    stage1payoff = models.CurrencyField(initial=0)
    stage2payoff = models.CurrencyField(initial=0)
    city_order = models.BooleanField()
    calculable = models.BooleanField(initial=False)

    def get_part2_instructions_path(self):
        return f'trust/includes/instructions/part2_instructions_{self.role()}.html'

    def get_part2_examples_path(self):
        return f'trust/includes/instructions/part2_examples_{self.role()}.html'

    def set_params(self):
        """create some params and decision sets that we can create before role assignment. Which are:
        averages, and order in which cities are shown."""
        p = self
        p.create_averages()
        # randomize city order
        p.participant.vars['city_order'] = random.choice([True, False])
        p.city_order = p.participant.vars['city_order']

    def assign_role(self):
        """Assign a role, and create decisions and beliefs questions based on that role.
        We correct to the fact that new groups start forming from 2 (1 is first large group for all).
        and taking into account the fact that we now get groups of single players, we just cycle over roles
        in formed group"""
        roles = list(Constants.roles.keys())
        self._role = roles[
            (self.group.id_in_subsession - 2) % 2]  # odd numbers become Senders, even numbers become Receivers
        self.create_decisions()
        self.create_beliefs()

    @property
    def role_desc(self):
        """Returns a friendly description of a players' role """
        return Constants.roles.get(self.role())

    def get_city_obj(self):
        return self.city

    @property
    def guess_desc(self):
        if self.role() == 'sender':
            return c(self.guess)
        else:
            return 'не передать свою начальную сумму' if self.guess == 0 else 'передать свою начальную сумму'

    @property
    def decision_desc(self):
        if self.role() == 'sender':
            return 'не передать свою начальную сумму' if self.decision == 0 else 'передать свою начальную сумму'
        else:
            return f'вернуть {c(self.decision)}'

    @property
    def other_role_desc(self):
        """Returns a friendly description of a role of another player"""
        other_role = 'receiver' if self.role() == 'sender' else 'sender'
        return Constants.roles.get(other_role)

    def role(self):
        return self._role

    def create_decisions(self):
        if self.role() == 'sender':
            self.create_sender_decisions()
        else:
            self.create_receiver_decisions()

    def create_beliefs(self):
        if self.role() == 'sender':
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
        ds = [Decision(city=city, owner=self, decision_type=decision_type) for city in City.objects.all()]
        Decision.objects.bulk_create(ds)

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
