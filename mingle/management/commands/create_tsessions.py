from django.core.management.base import BaseCommand
import logging
from otree.session import create_session
from trust.models import City

logger = logging.getLogger(__name__)


def session_creator(num_participants, stub):
    cities = City.objects.all().order_by('code')
    for x in cities:
        logger.info(f'Creating session for city: {x.eng}; participants:{num_participants} ')
        s = create_session(
            session_config_name='full_ru',
            num_participants=num_participants,
            label=f'{stub}: {x.eng}',
            modified_session_config_fields=dict(city_code=x.code,
                                                toloka=True,
                                                toloka_sandbox=False,
                                                )
        )
        s.comment = s.label
        s.save()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('num_participants', help='Number of participants per session.', type=int)

    def handle(self, num_participants, *args, **options):
        logger.warning('This command will create a bunch of sessions for each city for toloka')
        stub = input("Enter stub : ")
        session_creator(num_participants, stub)
