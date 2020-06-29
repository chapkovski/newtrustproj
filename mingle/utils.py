from django.db import connection
from time import time
import logging

logger = logging.getLogger(__name__)


def time_check(func):
    def wrapper(*args, **kwargs):
        startq = len(connection.queries)
        start_time = time()
        func(*args, **kwargs)
        endq = len(connection.queries)
        logger.info(f'FUNC: {func.__name__}; Total queries: {endq - startq}; Total time: {time() - start_time}',)

    return wrapper
