from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class TrustConfig(AppConfig):
    name = 'trust'

    def ready(self):

        t = settings.TEMPLATES[0]
        t['OPTIONS']['builtins'] = [
            'otree.templatetags.otree',
            'django.templatetags.i18n'
        ]

        try:
            City = self.get_model('City')
            for i in settings.CITIES:
                City.objects.get_or_create(code=i['code'], defaults={'description': i['name'],
                                                                     'eng': i['eng']})

        except (OperationalError, ProgrammingError) as e:
            logger.warning(e)
            logger.warning('No city table found')
