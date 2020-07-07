from django.apps import AppConfig
from django.db.utils import OperationalError

class MingleConfig(AppConfig):
    name = 'mingle'

    def ready(self):
        print('MINGLE READY')
        from . import signals  # noqa
        from otree.models import Session
        try:
            print(Session.objects.all())
        except OperationalError:
            pass