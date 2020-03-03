from otree.api import Currency as c, currency_range
from .pages import *
from ._builtin import Bot
from .models import Constants, Player


class PlayerBot(Bot):
    def play_round(self):
        for page in page_sequence:
            fields = {}
            for i in page.form_fields:
                if i == 'age':
                    fields[i] = 13
                else:
                    fields[i] = 1
            yield page, fields
