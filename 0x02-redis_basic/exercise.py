#!/usr/bin/env python3
"""
A module for using the Redis NoSQL database
"""

import uuid
from functools import wraps
from typing import Callable, Optional, TypeVar, Union, cast

import redis

T = TypeVar('T', str, bytes, int, float)


def count_calls(method: Callable) -> Callable:
    """
    Count the number of calls to a function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """
    Cache class for redis
    """

    def __init__(self) -> None:
        """Init method for Cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
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
        # Ensure data is bytes
        assert isinstance(data, bytes), "Expected data to be bytes"
        if fn is not None:
            return fn(data)
        return cast(T, data)

    def get_str(self, key: str) -> Optional[str]:
        """Get string data from redis database"""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        return self.get(key, fn=int)
