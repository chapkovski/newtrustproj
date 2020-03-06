from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class Code(Page):
    form_model = 'player'
    form_fields = ['city']
    a = 1

    def city_error_message(self, value):
        if value not in self.subsession.cities:
            return 'Пожалуйста, проверьте код города'

    def before_next_page(self):
        if self.timeout_happened:
            self.player.city = random.choice(self.subsession.cities)
            self.participant.vars['bot_marker'] = 'BOT-'
        self.participant.vars['city'] = self.player.city


class Welcome(Page):
    form_fields = ['pc_id']
    form_model = 'player'

    def before_next_page(self):
        if self.timeout_happened:
            self.player.pc_id = random.randint(10000, 100000)
            self.participant.vars['bot_marker'] = 'BOT-'
        self.participant.vars['pc_id'] = self.player.pc_id
        bot_marker = self.participant.vars.get('bot_marker', '')
        self.participant.label = f'{bot_marker}{self.player.city}-{self.player.pc_id}'


page_sequence = [Code, Welcome]
