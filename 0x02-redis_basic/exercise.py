#!/usr/bin/env python3
"""
Writing strings to Redis.
"""
import redis
import uuid
from typing import Union


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

    def store(self, data: 'Union[str, bytes, int, float]') -> str:
        key = str(uuid.uuid4())
        self._redis.mset({key: data})
        return key
