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
from django.db.utils import OperationalError

author = 'Philipp Chapkovski, '

doc = """
Sorter app that guarantees the proper matching for further trust game.
"""


class Constants(BaseConstants):
    name_in_url = 'sorter'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    @property
    def cities(self):
        return [self.session.config.get('city1'), self.session.config.get('city2')]

    def creating_session(self):
        if self.session.num_participants % 2 != 0: raise Exception('Number of participants should be even!')
        try:
            for i in settings.CITIES:
                City.objects.get_or_create(code=i['code'], defaults={'description': i['name']})
        except OperationalError:
            print('no table is ready yet...')
        if len(self.cities) != len(set(self.cities)): raise Exception('Вы ввели два одинаковых города! Не надо так.')
        registered_cities = set(City.objects.all().values_list('code', flat=True))
        if not set(self.cities).issubset(registered_cities): raise Exception(
            'Вы ввели неверный код для одного из городов!')


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    city = models.StringField()


class City(djmodels.Model):
    code = models.StringField(unique=True)
    description = models.StringField(unique=True)

    def __str__(self):
        return f'Code: {self.code}; Description: {self.description}'
