"""
UserProvider
"""
import json
from datetime import datetime
from typing import Optional

from google.cloud.firestore_v1 import DocumentSnapshot, FieldFilter
from redis.asyncio import Redis

from app.clients.firebase.firestore import GoogleFirestoreClient
from app.libs.consts.enums import ExpireTime
from app.libs.consts.redis_keys import get_user_key
from app.libs.database import RedisPool
from app.libs.decorators.sentry_tracer import distributed_trace
from app.schemas.user import User


class UserProvider:
    """UserProvider"""

    def __init__(self, redis: RedisPool):
        self._redis: Redis = redis.create()
        self.firestore_client = GoogleFirestoreClient()

    @distributed_trace()
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

    @distributed_trace()
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

    @distributed_trace()
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Get user by id
        :param user_id:
        :return:
        """
        redis_key = get_user_key(user_id=user_id)
        if await self._redis.exists(redis_key):
            user_data = await self._redis.get(redis_key)
            return User(**json.loads(user_data))
        raw_user: DocumentSnapshot = await self.firestore_client.get_document(
            collection="users",
            document=user_id
        )
        if not raw_user.exists:
            return None
        user = User(**raw_user.to_dict())
        await self._redis.set(
            name=redis_key,
            value=user.model_dump_json(),
            ex=ExpireTime.ONE_WEEK.value
        )
        return user

    @distributed_trace()
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
        await self._redis.delete(get_user_key(user_id=user_id))
