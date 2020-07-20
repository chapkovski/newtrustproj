import logging
from tolokaregister.models import TolokaParticipant
from ._uni_toloka_command import TolokaCommand

logger = logging.getLogger(__name__)


class Command(TolokaCommand):
    command_desc = 'updating info'

    def do_over_single(self, p, sandbox=False):
        defaults = dict(assignment=p.label, sandbox=sandbox)
        tp, created = TolokaParticipant.objects.get_or_create(owner=p, defaults=defaults)
        if created:
            logger.info(f'tparticipant was created for participant {p.code}')
        else:
            logger.info(f'tparticipant {tp.id} is already created for participant {p.code}')
        tp.get_info()
        logger.info(f'participant {p.code}: status: {tp.status} ')
