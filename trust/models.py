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

author = 'Philipp Chapkovski'

doc = """
Interregional trust game. 
"""


class Constants(BaseConstants):
    name_in_url = 'trust'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    matched_different = models.BooleanField(default=True)

    @property
    def cities(self):
        return set([self.session.config.get('city1'), self.session.config.get('city2')])

    def creating_session(self):
        registered_cities = set(City.objects.all().values_list('code', flat=True))
        if not self.cities.issubset(registered_cities): raise Exception('Вы ввели неверный код для одного из городов!')


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    def role(self):
        return 'Sender' if self.id_in_subsession % 2 == 1 else 'Receiver'

    city = models.StringField()


class City(djmodels.Model):
    code = models.StringField()
    description = models.StringField()

    def __str__(self):
        return f'Code: {self.code}; Description: {self.description}'


class Decision(djmodels.Model):
    city = djmodels.ForeignKey(to=City, on_delete=djmodels.CASCADE)
    owner = djmodels.ForeignKey(to=Player, on_delete=djmodels.CASCADE)

    class Meta:
        abstract = True


class SenderDecision(Decision):
    send = models.BooleanField()


class ReturnDecision(Decision):
    send_back = models.IntegerField()


class SenderBeliedReturn(Decision):
    belief_on_return = models.IntegerField()


class ReturnerBeliefSend(Decision):
    belief_on_send = models.BooleanField()
