"""Simple profiling timer."""

import time
import functools
from collections import namedtuple


Result = namedtuple("Result", "func_name spent avg returned")


def timer(_number=1):
    """Decorator that measures time spent on the execution.

    Args:
        _number (int): define how many times the functions will run.

    Returns:
        Instance of Result namedtuple.
    """
    def outer(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if type(_number) != int or _number < 1:
                raise Exception('argument "_number" must be a positive integer.')

            start_time = time.time()
            for i in range(_number):
                try:
                    returned = func(*args, **kwargs)
                except Exception as exception:
                    returned = exception

            finish_time = time.time()
            time_spent = finish_time - start_time
            average_time = time_spent / _number
            return Result(func.__name__, time_spent, average_time, returned)

        return wrapper
    return outer
