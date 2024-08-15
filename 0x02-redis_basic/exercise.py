#!/usr/bin/env python3
"""
A module for using the Redis NoSQL database
"""

import uuid
from functools import wraps
from typing import Callable, Optional, TypeVar, Union, cast, Any

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


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and
    outputs for a particular function.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Wrapper function to store call history and execute the method."""
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:outputs".format(method.__qualname__)

        # Convert arguments to string and store in the Redis list
        self._redis.rpush(input_key, str(args))

        # Execute the original method and get the output
        output = method(self, *args, **kwargs)

        # Store the output in the Redis list
        self._redis.rpush(output_key, str(output))

        return output

    return wrapper


class Cache:
    """
    Cache class for redis
    """

    def __init__(self) -> None:
        """Init method for Cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
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
