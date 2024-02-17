"""
UserHandler
"""
import uuid
from datetime import datetime
from typing import Optional

import bcrypt
from asyncpg import UniqueViolationError
from redis.asyncio import Redis
from starlette import status

from app.exceptions.api_base import APIException
from app.handlers import AuthHandler
from app.libs.consts.enums import ExpireTime, StatusBase
from app.libs.consts.redis_keys import get_user_access_token_key, get_user_otp_secret_key
from app.libs.database import RedisPool
from app.libs.decorators.sentry_tracer import distributed_trace
from app.providers import UserProvider
from app.schemas.user import User
from app.serializers.v1.user import UserLogin, UserRegister, LoginResponse, UserInfoResponse, UserBase, OTPInfo, TwoFactorVerify, TokenResponse, ChangePassword


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
            last_login=user.last_login_at,
            two_factor_status=StatusBase.ENABLED if user.otp_active else StatusBase.DISABLED
        )

    @distributed_trace()
    async def login(self, model: UserLogin) -> LoginResponse:
        """
        Login
        redirect
        :return:
        """
        user: Optional[User] = await self.user_provider.get_user_by_username(username=model.username)
        if user is None:
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Unauthorized"
            )
        if user.is_active is False:
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Unauthorized"
            )
        if not self.check_password(input_password=model.password, hashed_password=user.hash_password.encode()):
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Unauthorized"
            )
        if user.otp_secret:
            two_factor_token = self.auth_handler.generate_2fa_token(user=user)
            return LoginResponse(
                access_token=two_factor_token,
                two_factor_status=StatusBase.ENABLED
            )
        await self.update_last_login(user_id=user.id)
        access_token = self.auth_handler.generate_token(user=user)
        await self.redis.set(
            name=get_user_access_token_key(user_id=user.id),
            value=access_token,
            ex=ExpireTime.ONE_DAY.value * 3
        )
        return LoginResponse(access_token=access_token)

    @distributed_trace()
    async def two_factor_auth_verify(self, user_id: uuid.UUID, model: TwoFactorVerify) -> TokenResponse:
        """
        Two-factor auth verify
        :param user_id:
        :param model:
        :return:
        """
        user: Optional[User] = await self.user_provider.get_user_by_id(user_id=user_id)
        if user is None:
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Unauthorized"
            )
        if not user.otp_secret:
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="2FA not enabled"
            )
        if not self.auth_handler.verify_otp(secret=user.otp_secret, otp=model.otp):
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="2FA verification failed"
            )
        await self.update_last_login(user_id=user.id)
        access_token = self.auth_handler.generate_token(user=user)
        await self.redis.set(
            name=get_user_access_token_key(user_id=user.id),
            value=access_token,
            ex=ExpireTime.ONE_DAY.value * 3
        )
        return TokenResponse(access_token=access_token)

    async def update_last_login(self, user_id: uuid.UUID):
        """
        Update last login
        :param user_id:
        :return:
        """
        last_login = datetime.now()
        await self.user_provider.update_last_login(user_id=user_id, last_login=last_login)

    @distributed_trace()
    async def change_password(self, user_id: uuid.UUID, model: ChangePassword):
        """
        Change password
        :param user_id:
        :param model:
        :return:
        """
        user: Optional[User] = await self.user_provider.get_user_by_id(user_id=user_id)
        if user is None:
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Unauthorized"
            )
        if user.otp_active and not model.otp:
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="2FA verification required"
            )
        if user.otp_secret and not self.auth_handler.verify_otp(secret=user.otp_secret, otp=model.otp):
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="2FA verification failed"
            )
        if not self.check_password(input_password=model.old_password, hashed_password=user.hash_password.encode()):
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Unauthorized"
            )
        if not self.auth_handler.verify_password_strength(password=model.new_password):
            raise APIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Password not strong enough"
            )
        if model.new_password != model.confirm_password:
            raise APIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Password not match"
            )
        if user.hash_password == self.hash_password(user.password_salt.encode(), model.new_password).decode():
            raise APIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="The new password is the same as the old password"
            )
        salt = bcrypt.gensalt()
        hash_password = self.hash_password(salt, model.new_password)
        await self.user_provider.change_password(
            user_id=user_id,
            password=hash_password.decode(),
            salt=salt.decode()
        )

    @distributed_trace()
    async def reset_2fa(self, user_id: uuid.UUID, model: TwoFactorVerify):
        """
        Reset 2fa
        :param user_id:
        :param model:
        :return:
        """
        user: Optional[User] = await self.user_provider.get_user_by_id(user_id=user_id)
        if user is None:
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Unauthorized"
            )
        if not user.otp_secret:
            raise APIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="2FA not enabled"
            )
        if not self.auth_handler.verify_otp(secret=user.otp_secret, otp=model.otp):
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="2FA verification failed"
            )
        await self.user_provider.reset_otp_secret(user_id=user_id)

    @distributed_trace()
    async def generate_new_otp_info(self, user_id: uuid.UUID) -> OTPInfo:
        """
        Generate new otp info
        :return:
        """
        secret = self.auth_handler.generate_otp_secret()
        otp_uri = self.auth_handler.generate_otp_uri(user_id=user_id, secret=secret)
        await self.redis.set(
            name=get_user_otp_secret_key(user_id=user_id),
            value=secret,
            ex=ExpireTime.ONE_DAY.value
        )
        return OTPInfo(secret=secret, uri=otp_uri)

    @distributed_trace()
    async def verify_otp(self, user_id: uuid.UUID, previous_otp: str, otp: str):
        """
        Verify otp
        :param user_id:
        :param previous_otp:
        :param otp:
        :return:
        """
        secret = await self.redis.get(get_user_otp_secret_key(user_id=user_id))
        result = self.auth_handler.verify_new_otp(secret=secret, previous_otp=previous_otp, otp=otp)
        if not result:
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="2FA verification failed"
            )
        await self.redis.delete(get_user_otp_secret_key(user_id=user_id))
        await self.user_provider.update_otp_secret(user_id=user_id, otp_secret=secret)
