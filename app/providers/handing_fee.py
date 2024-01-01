"""
HandingFeeProvider
"""
from app.clients.firebase.firestore import GoogleFirestoreClient
from app.libs.database import RedisPool


class HandingFeeProvider:
    """HandingFeeProvider"""

    def __init__(self, redis: RedisPool):
        self._redis = redis.create()
        self.firestore_client = GoogleFirestoreClient()

    async def set_global_handing_fee(self, data: dict):
        """
        set global handing fee
        :param data:
        :return:
        """
        await self.firestore_client.set_document(
            collection="handing_fee",
            document="global",
            data=data
        )

    async def get_global_handing_fee(self):
        """
        get global handing fee
        :return:
        """
        result = await self.firestore_client.get_document(
            collection="handing_fee",
            document="global"
        )
        return result.to_dict()

    async def get_handing_fee(self, group_id: str):
        """
        get handing fee
        :param group_id:
        :return:
        """
        result = await self.firestore_client.get_document(
            collection="handing_fee",
            document=group_id
        )
        return result.to_dict()

    async def update_handing_fee(self, group_id: str, data: dict):
        """
        set handing fee
        :param group_id:
        :param data:
        :return:
        """
        await self.firestore_client.set_document(
            collection="handing_fee",
            document=group_id,
            data=data
        )

