"""
HandingFeeProvider
"""
from app.libs.database import RedisPool
from app.libs.decorators.sentry_tracer import distributed_trace


class HandingFeeProvider:
    """HandingFeeProvider"""

    def __init__(self, redis: RedisPool):
        self._redis = redis.create()

    @distributed_trace()
    async def set_global_handing_fee(self, data: dict):
        """
        set global handing fee
        :param data:
        :return:
        """

    @distributed_trace()
    async def get_global_handing_fee(self):
        """
        get global handing fee
        :return:
        """

    @distributed_trace()
    async def get_handing_fee(self, group_id: str):
        """
        get handing fee
        :param group_id:
        :return:
        """

    @distributed_trace()
    async def update_handing_fee(self, group_id: str, data: dict):
        """
        set handing fee
        :param group_id:
        :param data:
        :return:
        """
