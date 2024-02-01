"""
UserHandler
"""
import uuid
from datetime import datetime
from typing import Optional

import bcrypt
import pytz
from asyncpg import UniqueViolationError
from redis.asyncio import Redis
from starlette import status

from app.exceptions.api_base import APIException
from app.handlers import AuthHandler
from app.libs.consts.enums import ExpireTime
from app.libs.consts.redis_keys import get_user_access_token_key
from app.libs.database import RedisPool
from app.libs.decorators.sentry_tracer import distributed_trace
from app.schemas.user import User
from app.providers import UserProvider
from app.serializers.v1.user import UserLogin, UserRegister, LoginResponse, TokenResponse, UserInfoResponse, UserBase


class UserHandler:
    """UserHandler"""

    def __init__(
        self,
        redis: RedisPool,
        auth_handler: AuthHandler,
        user_provider: UserProvider
    ):
        self.redis: Redis = redis.create()
        self.auth_handler = auth_handler
        self.user_provider = user_provider

    @staticmethod
    def hash_password(salt: bytes, password: str) -> bytes:
        """

        :param salt:
        :param password:
        :return:
        """
        return bcrypt.hashpw(password.encode(), salt)

    @staticmethod
    def check_password(input_password: str, hashed_password: bytes) -> bool:
        """

        :param input_password:
        :param hashed_password:
        :return:
        """
        return bcrypt.checkpw(input_password.encode(), hashed_password)

    @distributed_trace()
    async def check_user_exist(self, username: str) -> bool:
        """
        Check user exist
        :param username:
        :return:
        """
        user = await self.user_provider.get_user_by_username(username=username)
        if not user:
            return False
        return user.username == username

    @distributed_trace()
    async def register(self, model: UserRegister) -> UserBase:
        """
        Register
        :return:
        """
        if model.password != model.confirm_password:
            raise APIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Password not match"
            )
        if await self.check_user_exist(username=model.username):
            raise APIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="User already exist"
            )
        if not self.auth_handler.verify_password_strength(password=model.password):
            raise APIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Password not strong enough"
            )
        salt = bcrypt.gensalt()
        hash_password = self.hash_password(salt, model.password)
        user = User(
            id=model.id or uuid.uuid4(),
            email=model.email,
            username=model.username,
            display_name=model.display_name or model.username,
            hash_password=hash_password.decode(),
            password_salt=salt.decode(),
            is_active=True,
        )
        try:
            await self.user_provider.create_user(user=user)
        except UniqueViolationError:
            raise APIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="User already exist"
            )
        else:
            return UserBase(id=user.id)

    @distributed_trace()
    async def get_user_info(self, user_id: uuid.UUID) -> UserInfoResponse:
        """
        Get user info
        :param user_id:
        :return:
        """
        user: Optional[User] = await self.user_provider.get_user_by_id(user_id=user_id)
        if user is None:
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Unauthorized"
            )
        return UserInfoResponse(
            id=user.id,
            username=user.username,
            display_name=user.display_name,
            is_active=user.is_active,
            last_login=user.last_login_at
        )

    @distributed_trace()
    async def login(self, model: UserLogin) -> LoginResponse:
        """
        Login
        :return:
        """
        user: Optional[User] = await self.user_provider.get_user_by_username(username=model.username)
        if user is None:
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Unauthorized"
            )
        if not self.check_password(input_password=model.password, hashed_password=user.hash_password.encode()):
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Unauthorized"
            )
        last_login = datetime.now()
        await self.user_provider.update_last_login(user_id=user.id, last_login=last_login)
        access_token = self.auth_handler.generate_token(user=user)
        await self.redis.set(
            name=get_user_access_token_key(user_id=user.id.hex),
            value=access_token,
            ex=ExpireTime.ONE_DAY.value * 3
        )
        return LoginResponse(access_token=access_token)
