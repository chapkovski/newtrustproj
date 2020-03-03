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
    pc_id = models.IntegerField(label='')

    def pc_id_error_message(self, value):
        ids = self.subsession.player_set.filter(pc_id__isnull=False, city=self.city).values_list("pc_id", flat=True)
        if value in ids:
            return 'Пожалуйста, проверьте номер участника. Этот номер уже используется'
