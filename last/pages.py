from otree.api import Currency as c, currency_range
from ._builtin import WaitPage
from questionnaire.generic_pages import Page
from .models import Constants


class Results(Page):
    pass


page_sequence = [
    Results
]
