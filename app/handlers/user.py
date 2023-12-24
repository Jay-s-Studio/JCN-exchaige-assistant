"""
UserHandler
"""
import uuid
from datetime import datetime
from typing import Optional

import bcrypt
import pytz

from app.models.user import User
from app.providers import UserProvider
from app.serializers.v1.user import UserLogin, UserRegister, LoginResponse


class UserHandler:
    """UserHandler"""

    def __init__(self, user_provider: UserProvider):
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
        salt = bcrypt.gensalt()
        hash_password = self.hash_password(salt, model.password)
        user = User(
            id=uuid.uuid4(),
            username=model.username,
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
        return LoginResponse(
            access_token="",
        )
