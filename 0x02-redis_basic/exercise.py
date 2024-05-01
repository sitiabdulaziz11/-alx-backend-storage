#!/usr/bin/env python3
"""
Writing strings to Redis
"""
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

    def store(self, data: any) -> str:
        Randk = str(uuid.uuid4())
        self._redis.set(Randk, data)
        return Randk
