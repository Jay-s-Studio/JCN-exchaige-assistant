"""
UserHandler
"""
import uuid
from datetime import datetime
from typing import Optional

import bcrypt
import pytz
from fastapi import HTTPException
from redis.asyncio import Redis
from starlette import status

from app.handlers import AuthHandler
from app.libs.consts.redis_keys import get_user_access_token_key
from app.libs.database import RedisPool
from app.models.user import User
from app.providers import UserProvider
from app.serializers.v1.user import UserLogin, UserRegister, LoginResponse, TokenResponse


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
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    @staticmethod
    def check_password(input_password: str, hashed_password: bytes) -> bool:
        """

        :param input_password:
        :param hashed_password:
        :return:
        """
        return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password)

    async def check_user_exist(self, username: str) -> bool:
        """
        Check user exist
        :param username:
        :return:
        """
        user = await self.user_provider.get_user_by_username(username=username)
        if user is None:
            return False
        return user.username == username

    async def create_user(self, model: UserRegister):
        """
        Create user
        :return:
        """
        if await self.check_user_exist(username=model.username):
            raise Exception("User already exist")
        if not self.auth_handler.verify_password_strength(password=model.password):
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Password not strong enough"
                }
            )
        salt = bcrypt.gensalt()
        hash_password = self.hash_password(salt, model.password)
        user = User(
            id=uuid.uuid4(),
            username=model.username,
            display_name=model.username,
            hash_password=hash_password.decode('utf-8'),
            password_salt=salt.decode('utf-8'),
            is_active=True,
            created_at=datetime.now(tz=pytz.UTC)
        )
        user.model_dump()
        await self.user_provider.create_user(user=user)

    async def login(self, model: UserLogin) -> LoginResponse:
        """
        Login
        :return:
        """
        user: Optional[User] = await self.user_provider.get_user_by_username(username=model.username)
        if user is None:
            raise Exception("User not found")
        if not self.check_password(input_password=model.password, hashed_password=user.hash_password.encode('utf-8')):
            raise Exception("Password not correct")
        last_login = datetime.now(tz=pytz.UTC)
        await self.user_provider.update_last_login(user_id=user.id.hex, last_login=last_login)
        access_token = await self.auth_handler.generate_token(user=user)
        await self.redis.set(name=get_user_access_token_key(user_id=user.id.hex), value=access_token)
        return LoginResponse(
            **user.model_dump(exclude={"hash_password", "password_salt", "created_at", "last_login"}),
            last_login=last_login,
            access_token=access_token
        )

    async def refresh_token(self, user_id: str, token: str) -> TokenResponse:
        """
        Refresh token
        :param user_id:
        :param token:
        :return:
        """
        access_token = await self.redis.get(name=get_user_access_token_key(user_id=user_id))
        if access_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"message": "Unauthorized"}
            )
        if access_token != token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"message": "Unauthorized"}
            )
        user = await self.user_provider.get_user_by_id(user_id=user_id)
        if user is None:
            raise Exception("User not found")
        new_token = await self.auth_handler.generate_token(user=user)
        await self.redis.set(name=get_user_access_token_key(user_id=user_id), value=new_token)
        return TokenResponse(access_token=new_token)
