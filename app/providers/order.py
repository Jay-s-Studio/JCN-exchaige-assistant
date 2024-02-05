"""
OrderProvider
"""
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

    async def set_order(
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
            ex=ExpireTime.ONE_HOUR.value
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
