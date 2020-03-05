from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time


class Results(Page):
    pass
    # def post(self):
    #     if self.participant.is_browser_bot:
    #         time.sleep(30)
    #     return super().post()


page_sequence = [Results]
