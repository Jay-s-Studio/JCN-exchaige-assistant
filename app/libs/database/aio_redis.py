"""
AioRedis
"""
from typing import AsyncIterator

from redis.asyncio import Redis, from_url

from app.config import settings


async def redis_pool() -> AsyncIterator[Redis]:
    """redis pool"""
    uri = f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}"
    if settings.REDIS_SSL:
        uri = f"rediss://{settings.REDIS_USERNAME}:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}"
    session = from_url(
        url=uri,
        password=settings.REDIS_PASSWORD,
        encoding="utf-8",
        decode_responses=True
    )
    yield session
    session.close()
    await session.wait_closed()
