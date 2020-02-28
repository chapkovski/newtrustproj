from otree.api import Currency as c, currency_range
from .pages import *
from ._builtin import Bot
from .models import Constants

import random


class PlayerBot(Bot):
    def play_round(self):
        if self.player.role() == 'Sender':
            yield SenderDecisionP,
            yield SenderBeliefP,
        else:
            yield ReturnDecisionP,
            yield ReturnerBeliefP,
        yield Results
