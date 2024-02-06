"""
OrderProvider
"""
from typing import Optional
from uuid import UUID

from redis.asyncio import Redis

from app.config import settings
from app.libs.consts.enums import ExpireTime
from app.libs.database import Session, RedisPool
from app.schemas.order import OrderCache


class OrderProvider:
    """OrderProvider"""

    def __init__(
        self,
        session: Session,
        redis: RedisPool
    ):
        self._session = session
        self._redis: Redis = redis.create()

    @staticmethod
    def redis_name(name: str):
        """

        :return:
        """
        return f"{settings.APP_NAME}:{name}"

    async def create_order(
        self,
        group_id: int,
        order_id: UUID,
        order_info: OrderCache
    ):
        """
        set order
        :param group_id:
        :param order_id:
        :param order_info:
        :return:
        """
        redis_name = self.redis_name(name=f"order:{group_id}:{str(order_id)}")
        await self._redis.set(
            name=redis_name,
            value=order_info.model_dump_json(),
            ex=ExpireTime.ONE_HOUR.value * 2
        )

    async def update_order(
        self,
        group_id: int,
        order_id: UUID,
        order_info: OrderCache
    ):
        """
        update order
        :param group_id:
        :param order_id:
        :param order_info:
        :return:
        """
        redis_name = self.redis_name(name=f"order:{group_id}:{str(order_id)}")
        expire_time = await self._redis.ttl(self.redis_name(name=f"order:{group_id}:{str(order_id)}"))
        await self._redis.set(
            name=redis_name,
            value=order_info.model_dump_json(),
            ex=expire_time
        )

    async def get_order(self, group_id: int, order_id: UUID) -> OrderCache:
        """
        get order
        :param group_id:
        :param order_id:
        :return:
        """
        redis_name = self.redis_name(name=f"order:{group_id}:{str(order_id)}")
        order_info = await self._redis.get(redis_name)
        return OrderCache.model_validate_json(order_info) if order_info else None

    async def get_order_by_group_id(self, group_id: int) -> Optional[OrderCache]:
        """
        get order by group id
        :param group_id:
        :return:
        """
        redis_name = self.redis_name(name=f"order:{group_id}:*")
        keys = await self._redis.keys(redis_name)
        if not keys:
            return None
        order_info = await self._redis.get(keys[0])
        return OrderCache.model_validate_json(order_info) if order_info else None
