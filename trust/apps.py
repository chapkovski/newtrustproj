from django.apps import AppConfig
from django.conf import settings
from django.db.utils import OperationalError

class TrustConfig(AppConfig):
    name = 'trust'

    def ready(self):
        print('READY?')
        from .models import City
        try:
            for i in settings.CITIES:
                City.objects.get_or_create(code=i['code'], defaults={'description': i['name']})
        except OperationalError:
            print('no table is ready yet...')
