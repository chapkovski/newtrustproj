from otree.api import Submission
from . import pages
from ._builtin import Bot


class PlayerBot(Bot):
    def play_round(self):
        yield pages.Code, {'city': 'Some city'}
