from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Code(Page):
    form_model = 'player'
    form_fields = ['city']
    a = 1

    def city_error_message(self, value):
        if value not in self.subsession.cities:
            return 'Пожалуйста, проверьте код города'

    def before_next_page(self):
        self.participant.vars['city'] = self.player.city


class Welcome(Page):
    form_fields = ['pc_id']
    form_model = 'player'

    def before_next_page(self):
        self.participant.vars['pc_id'] = self.player.pc_id
        self.participant.label = f'{self.player.city}-{self.player.pc_id}'


page_sequence = [Code, Welcome]
