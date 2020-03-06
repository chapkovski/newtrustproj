from otree.api import Currency as c, currency_range, Submission
from . import pages
from ._builtin import Bot
from .models import Constants
import random
from django.conf import settings
from django.db.utils import OperationalError


class PlayerBot(Bot):
    def play_round(self):
        bi = [True, False]
        proper_city = random.choice(['01', '02'])

        yield Submission(pages.Code, {'city': proper_city},
                         timeout_happened=False)
        yield Submission(pages.Welcome, {'pc_id': self.player.id_in_subsession}, timeout_happened=False)
