from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random
from django.conf import settings
from django.db.utils import OperationalError
from .models import City

try:
    for i in settings.CITIES:
        City.objects.get_or_create(code=i['code'], defaults={'description': i['name']})
except OperationalError:
    print('no table is ready yet...')


class PlayerBot(Bot):
    def play_round(self):
        if self.player.id_in_subsession < .6 * self.session.num_participants:
            city = 'MSK'
        else:
            city = 'SPB'
        yield pages.Code, {'city': city}
