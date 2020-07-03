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

decision_types = ['sender_decision', 'return_decision', 'sender_belief', 'receiver_belief', 'average_on_send_belief',
                  'average_on_return_belief']


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
    roles = {'sender': _('А'), 'receiver': _('Б')}
    cities = settings.CITIES
    cqs = settings.CQS
    max_cq_attempts = 2  # number of attempts after a person made an error in comp. question
    general_error_msg = {
        1: _('Не все Ваши ответы были правильными. Пожалуйста, прочтите еще раз инструкции в верхней части экрана, и исправьте свои ответы.'),
        2: _('Некоторые ответы все еще не правильны. Пожалуйста, исправьте их.'),
        3: _('Ответы, отмеченные ниже все еще не правильны. Пожалуйста, ознакомьтесь с правильными  решениями и ответами и приступайте к эксперименту'),
    }
    DEFAULT_CQ_ERROR = dict(rus='Пожалуйста, проверьте правильность вашего ответа.',
                            eng='Please, check your answer.')
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

    @time_check
    def creating_session(self):
        self.session_config_dump = json.dumps(self.session.config, cls=MyEncoder)
        if self.session.num_participants % 2 != 0:
            raise Exception('Number of participants should be even!')
        for i in settings.CITIES:
            City.objects.get_or_create(code=i['code'], defaults={'description': i['name'],
                                                                 'eng': i['eng']})
        cur_city = self.session.config.get('city_code')
        try:
            city_in = City.objects.get(code=cur_city)
        except City.DoesNotExist:

            raise Exception(_('Вы ввели неверный код для одного из городов!'))
        """We get the city and assign its objects to all players"""
        decisions = []
        ps = self.player_set.all()
        cities = City.objects.all()
        cqs = []
        for p in ps:
            for d in decision_types:
                ds = [Decision(city=city, owner=p, decision_type=d) for city in cities]
                decisions.extend(ds)
            for k, v in Constants.cqs.items():
                cqs.append(CQ(source=k, part=v.get('part'),
                              role=v.get('role'),
                              owner=p))
        ps.update(city=city_in)
        Decision.objects.bulk_create(decisions)
        CQ.objects.bulk_create(cqs)

        # TODO: add requirements to plug toloka pool and project ids
        # toloka_project_id
        # toloka_pool_id


class Group(BaseGroup):
    def set_players_params(self):
        for p in self.get_players():
            p.set_params()


class Player(BasePlayer):
    endowment = models.CurrencyField(initial=Constants.endowment)
    city = djmodels.ForeignKey(to='City', related_name='players', null=True, blank=True, on_delete=djmodels.SET_NULL)
    _role = models.StringField()
    stage1payoff = models.CurrencyField(initial=0)
    stage2payoff = models.CurrencyField(initial=0)
    city_order = models.BooleanField()
    calculable = models.BooleanField(initial=False)
    cq1_counter = models.FloatField()
    cq2_counter = models.FloatField()

    def get_part2_instructions_path(self):
        return f'trust/includes/instructions/part2_instructions_{self.role()}.html'

    def get_part2_examples_path(self):
        return f'trust/includes/instructions/part2_examples_{self.role()}.html'

    def set_params(self):
        """create some params and decision sets that we can create before role assignment. Which are:
        averages, and order in which cities are shown."""
        p = self
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


class Decision(djmodels.Model):
    city = djmodels.ForeignKey(to=City, on_delete=djmodels.CASCADE, null=True)
    owner = djmodels.ForeignKey(to=Player, on_delete=djmodels.CASCADE, related_name="decisions")
    decision_type = models.StringField(choices=decision_types)
    answer = models.IntegerField()
    forpd = DataFrameManager()
    objects = djmodels.Manager()


class CQ(djmodels.Model):
    """Actual cq for specific player. stores the number of wrong answers."""
    source = models.StringField()
    owner = djmodels.ForeignKey(to=Player, on_delete=djmodels.CASCADE, related_name="cqs")
    counter = models.IntegerField(initial=0)
    answer = models.IntegerField()
    part = models.IntegerField()
    role = models.StringField()

    def _lang(self):
        return self.owner.session.config.get('language', settings.LANGUAGE_CODE)

    @property
    def lang(self):
        if self._lang() == 'en':
            return 'eng'
        else:
            return 'rus'

    @property
    def choices(self):
        ch = Constants.cqs[self.source].get('choices')
        lang = self.lang
        if ch:
            return [(i['value'], i[lang]) for i in ch]

    @property
    def correct_answer(self):
        return Constants.cqs[self.source]['correct']

    @property
    def shown(self):
        if not self.role:
            return True
        return self.owner._role == self.role

    @property
    def text(self):
        return Constants.cqs[self.source]['text'][self.lang]

    @property
    def wrong_answer(self):
        lang = self.lang
        resp = [
            Constants.DEFAULT_CQ_ERROR[lang],
            Constants.cqs[self.source]['wrong1'][lang],
            Constants.cqs[self.source]['wrong2'][lang]
        ]
        if self.counter < len(resp):
            return resp[self.counter]
