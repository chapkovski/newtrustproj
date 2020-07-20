from django.core.management.base import BaseCommand
import logging
from otree.models import Session, Participant
from tolokaregister.models import TolokaParticipant

logger = logging.getLogger(__name__)


def update_info(p, sandbox=False):
    defaults = dict(assignment=p.label, sandbox=sandbox)
    tp, created = TolokaParticipant.objects.get_or_create(owner=p, defaults=defaults)
    if created:
        logger.info(f'tparticipant was created for participant {p.code}')
    else:
        logger.info(f'tparticipant {tp.id} is already created for participant {p.code}')
    tp.get_info()
    logger.info(f'participant {p.code}: status: {tp.status} ')


def process_single_session(code):
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
        logger.info(f'No toloka participants yet')
        return
    for p in participants:
        update_info(p)


def process_sessions(codes):
    for c in codes:
        process_single_session(c)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('sessioncodes', help='toloka session codes.', type=str)

    def handle(self, sessioncodes, *args, **options):
        logger.warning('This one will send a bunch of requests for toloka participants')
        confirmation = input("If you are sure you want to do this, type 'yes': ")
        if confirmation == 'yes':
            logger.info('gonna do this')
            session_codes = [i.strip() for i in sessioncodes.split(',')]
            process_sessions(session_codes)
        else:
            return
