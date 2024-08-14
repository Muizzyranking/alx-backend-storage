#!/usr/bin/env python3
"""
A module for using the Redis NoSQL database
"""

import redis
import uuid
from typing import Union


class Cache:
    """
    Cache class for redis
    """

    def __init__(self) -> None:
        """Init method for Cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in redis database"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
