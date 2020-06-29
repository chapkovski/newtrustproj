from django.db import connection
from time import time


def time_check(func):
    def wrapper(*args, **kwargs):
        startq = len(connection.queries)
        start_time = time()
        print("Something is happening before the function is called.")
        func(*args, **kwargs)
        print("Something is happening after the function is called.")
        endq = len(connection.queries)

        print(f'FUNC: {func.__name__}; Total queries: {endq - startq}')
        print(f'FUNC: {func.__name__}; Total time: {   time() - start_time}')

    return wrapper
