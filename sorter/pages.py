from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Code(Page):
    form_model = 'player'
    form_fields = ['city']

    def city_error_message(self, value):
        if value not in self.subsession.cities:
            return 'Please check the code!'

    def before_next_page(self):
        self.participant.vars['city'] = self.player.city


page_sequence = [Code, ]
