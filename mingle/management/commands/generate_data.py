from django.core.management.base import BaseCommand
from ._create_fake_data import data_creator
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('num_participants', help='Number of participants per session.', type=int)

    def handle(self, num_participants, *args, **options):
        logger.warning('This command will generate a random data for each of the city. For '
                       'internal test only!')

        data_creator(num_participants)
