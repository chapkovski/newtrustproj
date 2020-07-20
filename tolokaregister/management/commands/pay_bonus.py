from django.core.management.base import BaseCommand
import logging
from otree.session import create_session
from trust.models import City

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('num_participants', help='Number of participants per session.', type=int)

    def handle(self, num_participants, *args, **options):
        logger.warning('This command will create a bunch of sessions for each city for toloka')
        stub = input("Enter stub : ")
        session_creator(num_participants, stub)
