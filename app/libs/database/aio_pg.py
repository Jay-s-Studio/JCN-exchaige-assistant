import asyncio
from enum import Enum
from typing import Optional

import asyncpg

from app.config import settings

_AIO_DB_CONTEXTS = {}
_lock = False
__all__ = ['Keys', 'create_pool', 'setup', 'create_connection']


class Keys(Enum):
    DEFAULT = 'DEFAULT'
    POOL = 'POOL'


class AioDbContext:
    def __init__(
        self,
        key: str,
        schema: str = None,
        application_name: str = None,
        **connect_kwargs
    ):
        self.key: str = key
        self.schema: str = schema
        self.application_name: str = application_name
        self.pool: Optional[asyncpg.pool.Pool] = None
        self.connect_kwargs: dict = connect_kwargs


async def create_pool(
    key: Keys = Keys.POOL,
    command_timeout: int = None
) -> asyncpg.pool.Pool:
    global _lock
    context = _get_context(key)
    if not context:
        if key == Keys.POOL:
            context = setup(
                key,
                dsn=settings.SQLALCHEMY_DATABASE_URI,
                schema=settings.DATABASE_SCHEMA,
                application_name=settings.DATABASE_APPLICATION_NAME,
                min_size=0,
                max_size=100,
                command_timeout=command_timeout
            )
        else:
            raise TypeError(f'Failed to create connection pool, invalid database key "{key}", '
                            f'please register with setup first')
    if context.pool is not None:
        return context.pool
    if _lock:
        await asyncio.sleep(.1)
        return await create_pool(key)
    _lock = True
    server_settings = await create_server_settings(context)
    if command_timeout:
        context.connect_kwargs['command_timeout'] = command_timeout
    context.pool = await asyncpg.create_pool(
        server_settings=server_settings,
        max_inactive_connection_lifetime=60 * 10,
        **context.connect_kwargs)
    _lock = False
    return context.pool


async def create_connection(
    key: Keys = Keys.DEFAULT,
    command_timeout: int = None,
    loop=None,
    lock: asyncio.Lock = None
) -> asyncpg.Connection:
    if lock:
        await lock.acquire()
    try:
        context = _get_context(key)
        if not context:
            if key == Keys.DEFAULT:
                context = setup(
                    key,
                    dsn=settings.SQLALCHEMY_DATABASE_URI,
                    schema=settings.DATABASE_SCHEMA,
                    application_name=settings.DATABASE_APPLICATION_NAME,
                    command_timeout=command_timeout
                )
            else:
                raise TypeError(f'Failed to create connection pool, invalid database key "{key}", '
                                f'please register with setup first')
        server_settings = await create_server_settings(context)
        if command_timeout:
            context.connect_kwargs['command_timeout'] = command_timeout
        return await asyncpg.connect(
            server_settings=server_settings, **context.connect_kwargs, loop=loop)
    finally:
        lock and lock.release()


async def create_server_settings(context):
    if context.application_name:
        return {'application_name': context.application_name}
    return None


def setup(db=Keys.DEFAULT, application_name: str = None, **kwargs):
    if not kwargs:
        raise TypeError('kwargs is not null')
    key = db.value if isinstance(db, Keys) else str(db)
    if key in _AIO_DB_CONTEXTS:
        _AIO_DB_CONTEXTS[key].connect_kwargs = kwargs
    else:
        _AIO_DB_CONTEXTS[key] = AioDbContext(key, application_name=application_name, **kwargs)
    return _AIO_DB_CONTEXTS[key]


def _get_context(key: Keys = Keys.DEFAULT) -> AioDbContext:
    real_key = key.value if isinstance(key, Keys) else str(key)
    return _AIO_DB_CONTEXTS.get(real_key, None)
