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
from django.utils.translation import gettext_lazy as _
author = 'Philipp Chapkovski, '

doc = """
Sorter app that guarantees the proper matching for further trust game.
"""


class Constants(BaseConstants):
    name_in_url = 'sorter'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    city = models.StringField(label=_('В каком городе вы проживаете на данный момент?'))

