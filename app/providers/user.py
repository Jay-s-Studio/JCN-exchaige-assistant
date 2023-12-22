"""
UserProvider
"""
from typing import Optional

from google.cloud.firestore_v1 import DocumentSnapshot
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
        results = await collection.where("username", "==", username).get()
        raw_user: DocumentSnapshot = results[0]
        if not raw_user.exists:
            return None
        return User(**raw_user.to_dict())
