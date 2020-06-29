from django.db import connection
from time import time


def time_check(func):
    def wrapper(*args, **kwargs):
        startq = len(connection.queries)
        start_time = time()
        func(*args, **kwargs)
        endq = len(connection.queries)
        print(f'FUNC: {func.__name__}; Total queries: {endq - startq}')
        print(f'FUNC: {func.__name__}; Total time: {   time() - start_time}')

    return wrapper
