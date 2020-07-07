from django.apps import AppConfig
from django.db.utils import OperationalError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class TrustConfig(AppConfig):
    name = 'trust'
    def ready(self):
        try:
            City = self.get_model('City')
            for i in settings.CITIES:
                City.objects.get_or_create(code=i['code'], defaults={'description': i['name'],
                                                                     'eng': i['eng']})
            print(City.objects.all())
        except OperationalError:
            logger.warning('No city table found')

    def import_models(self):
        i = super().import_models()
        print(i)
        return i