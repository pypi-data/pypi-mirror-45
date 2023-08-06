"""Simple profiling timer."""

import time
import functools


def timer(func):
    """Decorator that measures time spent on the execution.

    Args:
        _number (int): define how many times the functions will run.

    Returns:
        Result of the last function's run.
    """
    @functools.wraps(func)
    def wrapper(_number=1, *args, **kwargs):
        if type(_number) != int or _number < 1:
            raise Exception('argument "_number" must be a positive integer.')

        start_time = time.time()
        for i in range(_number):
            try:
                result = func(*args, **kwargs)
            except Exception as exception:
                result = exception

        spent_time = time.time() - start_time
        return spent_time, result

    return wrapper
