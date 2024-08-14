#!/usr/bin/env python3
"""
A module for using the Redis NoSQL database
"""

import uuid
from typing import Callable, Optional, Union, TypeVar, cast

import redis

T = TypeVar('T', str, bytes, int, float)


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

    def get(self, key: str,
            fn: Optional[Callable[[bytes], T]] = None
            ) -> Optional[T]:
        """Get data from redis database"""

        data = self._redis.get(key)
        if data is None:
            return None
        assert isinstance(data, bytes), "Expected data to be bytes"
        if fn is not None:
            return fn(data)
        return cast(T, data)

    def get_str(self, key: str) -> Optional[str]:
        """Get string data from redis database"""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        return self.get(key, fn=int)
