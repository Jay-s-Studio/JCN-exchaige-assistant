"""
Util functions for lifespan
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter

from app.config import settings
from app.libs.database import RedisPool
from app.libs.logger import logger


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Lifespan
    :param _:
    """
    logger.info("Starting lifespan")
    redis_connection = RedisPool().create(db=1)
    logger.info(redis_connection)
    await FastAPILimiter.init(
        redis=redis_connection,
        prefix=f"{settings.APP_NAME}_limiter"
    )
    logger.info(FastAPILimiter.redis)
    logger.info(FastAPILimiter.prefix)
    try:
        yield
    finally:
        await FastAPILimiter.close()
