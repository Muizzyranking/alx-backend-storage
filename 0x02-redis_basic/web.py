import redis
import requests
from typing import Callable

# Initialize the Redis client
r = redis.Redis()


def cache_with_expiration(fn: Callable) -> Callable:
    """Decorator to cache the result of a function with an expiration time."""
    def wrapper(url: str) -> str:
        # Generate keys for caching and counting
        cache_key = f"cache:{url}"
        count_key = f"count:{url}"

        # Check if the URL is already cached
        cached_page = r.get(cache_key)
        if cached_page:
            # Increment the access count
            r.incr(count_key)
            return cached_page.decode('utf-8')

        # If not cached, fetch the content
        response = fn(url)

        # Store the content in the cache with a 10-second expiration
        r.setex(cache_key, 10, response)

        # Increment the access count
        r.incr(count_key)

        return response
    return wrapper


@cache_with_expiration
def get_page(url: str) -> str:
    """Fetch the HTML content of a URL and cache it with expiration."""
    response = requests.get(url)
    return response.text
