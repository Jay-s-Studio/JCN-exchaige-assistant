"""
UserProvider
"""
from datetime import datetime
from typing import Optional

from google.cloud.firestore_v1 import DocumentSnapshot, FieldFilter
from redis.asyncio import Redis

from app.clients.firebase.firestore import GoogleFirestoreClient
from app.libs.database import RedisPool
from app.models.user import User


class UserProvider:
    """UserProvider"""

    def __init__(self, redis: RedisPool):
        self._redis: Redis = redis.create()
        self.firestore_client = GoogleFirestoreClient()

    async def create_user(self, user: User) -> None:
        """
        Create user
        :param user:
        :return:
        """
        await self.firestore_client.set_document(
            collection="users",
            document=user.id.hex,
            data=user.model_dump()
        )

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username
        :param username:
        :return:
        """
        collection = self.firestore_client.gen_collection(collection="users")
        field_filter = FieldFilter(field_path="username", op_string="==", value=username)
        results = await collection.where(filter=field_filter).get()
        if not results:
            return None
        raw_user: DocumentSnapshot = results[0]
        if not raw_user.exists:
            return None
        return User(**raw_user.to_dict())

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Get user by id
        :param user_id:
        :return:
        """
        raw_user: DocumentSnapshot = await self.firestore_client.get_document(
            collection="users",
            document=user_id
        )
        if not raw_user.exists:
            return None
        return User(**raw_user.to_dict())

    async def update_last_login(self, user_id: str, last_login: datetime):
        """
        Update last login
        :param user_id:
        :param last_login:
        :return:
        """
        await self.firestore_client.update_document(
            collection="users",
            document=user_id,
            data={"last_login": last_login}
        )
