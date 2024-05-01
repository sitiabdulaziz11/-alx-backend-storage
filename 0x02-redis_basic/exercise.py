#!/usr/bin/env python3
"""
Writing strings to Redis
"""
import sys
from functools import wraps
from typing import Union, Optional, Callable
from uuid import uuid4

import redis


def count_calls(method: Callable) -> Callable:
    """
    Function that count how many
    times methods of the Cache class are called
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper method."""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Function add its input parameters to one list
    in redis, and store its output into another list.
    """
    key = method.__qualname__
    ip = "".join([key, ":inputs"])
    op = "".join([key, ":outputs"])

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper method"""
        self._redis.rpush(ip, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(op, str(res))
        return res

    return wrapper


class Cache:
    """
    Writing strings to Redis
    """

    def __init__(self):
        """
        Construct redis database
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Method used to store data in
        Redis with a randomly generated key
        """
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None) \
            -> Union[str, bytes, int, float]:
        """
        get method retrieves data from Redis using the specified key.
        It accepts an optional conversion function (fn) to convert the
        retrieved data back to the desired format.
        """
        if fn:
            return fn(self._redis.get(key))
        data = self._redis.get(key)
        return data

    def get_int(self: bytes) -> int:
        """
        Method which will automatically parameterize
        to integer.
        """
        return int.from_bytes(self, sys.byteorder)

    def get_str(self: bytes) -> str:
        """
        Method which will automatically parameterize
        to string.
        """
        return self.decode("utf-8")
