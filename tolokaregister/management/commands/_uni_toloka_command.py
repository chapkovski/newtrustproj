from django.core.management.base import BaseCommand
import logging
from otree.models import Session, Participant


logger = logging.getLogger(__name__)


class TolokaCommand(BaseCommand):
    command_desc = ''

    def do_over_single(self, p, sandbox=False):
        pass

    def process_sessions(self, codes):
        for c in codes:
            self.process_single_session(c)

    def process_single_session(self, code):
        try:
            s = Session.objects.get(code=code)
        except Session.DoesNotExist:
            logger.info(f'Session {code} is not found')
            return
        if not s.config.get('toloka'):
            logger.info(f'Session {code} is not toloka session')
            return
        participants = Participant.objects.filter(label__isnull=False, session=s)
        if not participants.exists():
            logger.info(f'Session {code}: No toloka participants yet')
            return
        for p in participants:
            self.do_over_single(p)

    def add_arguments(self, parser):
        parser.add_argument('sessioncodes', help='toloka session codes.', type=str)

    def handle(self, sessioncodes, *args, **options):
        logger.warning(f'This one will send a bunch of requests for toloka  doing WHAT: {self.command_desc}')
        confirmation = input("If you are sure you want to do this, type 'yes': ")
        if confirmation == 'yes':
            logger.info('gonna do this')
            session_codes = [i.strip() for i in sessioncodes.split(',')]
            self.process_sessions(session_codes)
        else:
            return
