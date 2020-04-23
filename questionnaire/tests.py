from otree.api import Currency as c, currency_range, Submission
from .pages import *
from ._builtin import Bot
from .models import Constants, Player

pass_html = ['RegionsIncome', 'RegionsKnowledge']
class PlayerBot(Bot):

    def play_round(self):

        for page in page_sequence:
            fields = {}
            for i in page.form_fields:
                if i == 'age':
                    fields[i] = 13
                else:
                    fields[i] = 1
            if page.__name__ in pass_html:
                yield Submission(page, fields, check_html=False)
            else:
                yield page, fields
