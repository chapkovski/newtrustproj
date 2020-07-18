from otree.api import Submission
from . import pages
from ._builtin import Bot


class PlayerBot(Bot):
    def play_round(self):
        yield pages.Intro,
        yield pages.Intro2,
        yield pages.ExchangeRate,
        yield Submission(pages.Code, {'city': 'Some city'}, check_html=False)
