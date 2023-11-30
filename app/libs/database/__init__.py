"""
Top-level package for database.
"""
from .aio_redis import redis_pool

__all__ = [
    "redis_pool",
]
