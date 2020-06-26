from django.core.management.base import BaseCommand
from ._create_fake_data import data_creator
import logging


logger = logging.getLogger(__name__)
class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.warning('This command will generate a random data for each of the city. For '
                       'internal test only!')
        num_participants = int(input('How many participants per session?'))
        data_creator(num_participants)