from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Results(Page):
    def post(self):
        import time
        time.sleep(5)
        return super().post()


page_sequence = [Results]
