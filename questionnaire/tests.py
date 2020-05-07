from otree.api import Currency as c, currency_range, Submission
from .pages import *
from ._builtin import Bot
from .models import Constants, Player

pass_html = ['RegionsIncome', 'RegionsKnowledge','Personal1', 'Personal2']
specific_values = dict(age=13,
                       occupation_child=11,
                       is_occupied=False,
                       self_employed=False)
class PlayerBot(Bot):

    def play_round(self):

        for page in page_sequence:
            fields = {}
            for i in page.form_fields:
                if i in specific_values.keys():
                    fields[i] = specific_values[i]
                else:
                    fields[i] = 1
            if page.__name__ in pass_html:
                yield Submission(page, fields, check_html=False)
            else:
                yield page, fields
