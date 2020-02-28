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



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    city = models.StringField()


