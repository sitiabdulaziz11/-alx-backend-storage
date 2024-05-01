#!/usr/bin/env python3
"""
Writing strings to Redis
"""
from typing import Callable, Union
import functools
import redis
import uuid


class Cache:
    """
    Writing strings to Redis
    """

    def __init__(self) -> None:
        """
        Construct redis database
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def count_calls(method: Callable) -> Callable:
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapper

    @count_calls
    def store(self, data: any) -> str:
        """
        Method used to store data in
        Redis with a randomly generated key
        """
        Randk = str(uuid.uuid4())
        self._redis.set(Randk, data)
        return Randk

    def get(self, key: str, fn: Callable = None) -> Union[
                                                        str, bytes, int,
                                                        float]:
        """
        get method retrieves data from Redis using the specified key.
        It accepts an optional conversion function (fn) to convert the
        retrieved data back to the desired format.
        """

        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Method which will automatically parameterize
        to string.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Method which will automatically parameterize
        to integer.
        """
        return self.get(key, fn=int)
