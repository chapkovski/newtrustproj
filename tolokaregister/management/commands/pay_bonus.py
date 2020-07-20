import logging
from tolokaregister.models import TolokaParticipant
from ._uni_toloka_command import TolokaCommand

logger = logging.getLogger(__name__)


class Command(TolokaCommand):
    command_desc = 'pay bonus'

    def do_over_single(self, p, sandbox=False):
        try:
            tp = TolokaParticipant.objects.get(owner=p)
        except TolokaParticipant.DoesNotExist:
            logger.info(f'No status known for participant {p.code}')
            return
        resp = tp.pay_bonus()
        error = resp.get('error')
        if error:
            logger.info(f"User {p.code}: {resp.get('errmsg')}")

        else:
            logger.info(f'User {p.code} bonus paid. Amount: {resp.get("amount")}')
