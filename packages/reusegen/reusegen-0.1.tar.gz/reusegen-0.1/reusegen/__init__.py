#
from types import GeneratorType, FunctionType
from functools import wraps


name = 'reusegen'

__all__ = [
    'reuse',
]


def reuse(obj):
    if isinstance(obj, GeneratorType):
        return reuse_generator(obj)
    elif isinstance(obj, FunctionType):
        return reuse_function(obj)


def reuse_function(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        return reuse_generator(func(*args, **kwds))
    return wrapper


def reuse_generator(gen):
    return Reuse(gen)


class Reuse:
    def __init__(self, gen):
        self._gen = gen
        self._cache = []
        self._first_run = True

    def __iter__(self):
        return ReuseIter(self)

    def _fetch_or_gen(self, index):
        cache_size = len(self._cache)
        assert index >= 0 and index <= cache_size
        if index == cache_size:
            if self._first_run:
                try:
                    self._cache.append(next(self._gen))
                except StopIteration:
                    self._first_run = False
            if not self._first_run:
                raise StopIteration
        return self._cache[index]


class ReuseIter:
    def __init__(self, reuse):
        self._reuse = reuse
        self._index = 0

    def __next__(self):
        self._index += 1
        return self._reuse._fetch_or_gen(self._index - 1)
