from functools import wraps
import time

__author__ = 'David Johnnes'
__email__ = "david.johnnes@gmail.com"


class Tower:

    @classmethod
    def debugger(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print("\t{} started execution".format(func.__name__))
            result = func(*args, **kwargs)
            print("\t{} ended execution".format(func.__name__))
            return result
        return wrapper

    @classmethod
    def timethis(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print("\t{} started at: {}".format(func.__name__, time.asctime()))
            result = func(*args, **kwargs)
            print("\t{} ended at: {}".format(func.__name__, time.asctime()))

            return result
        return wrapper
