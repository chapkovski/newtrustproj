from django.apps import AppConfig


class MingleConfig(AppConfig):
    name = 'mingle'

    def ready(self):
        print('MINGLE READY')
        from . import signals  # noqa