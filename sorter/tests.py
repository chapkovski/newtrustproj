from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random
from django.conf import settings
from django.db.utils import OperationalError



class PlayerBot(Bot):
    def play_round(self):
        if self.player.id_in_subsession < .6 * self.session.num_participants:
            city = 'MSK'
        else:
            city = 'SPB'
        yield pages.Code, {'city': city}
