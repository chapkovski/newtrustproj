from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random
from django.conf import settings
from django.db.utils import OperationalError



class PlayerBot(Bot):
    def play_round(self):
        yield pages.Code, {'city': random.choice(['07', '03'])}
        yield pages.Welcome, {'pc_id': self.player.id}
