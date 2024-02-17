"""
UserProvider
"""
import json
from datetime import datetime
from typing import Optional
from uuid import UUID

from redis.asyncio import Redis

from app.libs.consts.enums import ExpireTime
from app.libs.consts.redis_keys import get_user_key
from app.libs.database import RedisPool, Session
from app.libs.decorators.sentry_tracer import distributed_trace
from app.models import SysUser
from app.schemas.user import User


class UserProvider:
    """UserProvider"""

    def __init__(
        self,
        session: Session,
        redis: RedisPool
    ):
        self._session = session
        self._redis: Redis = redis.create()

    @distributed_trace()
    async def create_user(self, user: User) -> None:
        """
        Create user
        :param user:
        :return:
        """
        data = user.model_dump()
        try:
            await (
                self._session.insert(SysUser)
                .values(data)
                .execute()
            )
        except Exception as e:
            await self._session.rollback()
            raise e
        else:
            await self._session.commit()
        finally:
            await self._session.close()

    @distributed_trace()
    async def change_password(self, user_id: UUID, password: str, salt: str) -> None:
        """
        Change password
        :param user_id:
        :param password:
        :param salt:
        :return:
        """
        try:
            await (
                self._session.update(SysUser)
                .values(
                    hash_password=password,
                    password_salt=salt
                )
                .where(SysUser.id == user_id)
                .execute()
            )
        except Exception as e:
            await self._session.rollback()
            raise e
        else:
            await self._session.commit()
        finally:
            await self._session.close()

    @distributed_trace()
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username
        :param username:
        :return:
        """
        try:
            user = await (
                self._session.select(
                    SysUser.id,
                    SysUser.email,
                    SysUser.username,
                    SysUser.display_name,
                    SysUser.hash_password,
                    SysUser.password_salt,
                    SysUser.is_superuser,
                    SysUser.is_active,
                    SysUser.otp_active,
                    SysUser.otp_secret,
                    SysUser.last_login_at
                )
                .where(SysUser.username == username)
                .fetchrow(as_model=User)
            )
        except Exception as e:
            raise e
        else:
            return user
        finally:
            await self._session.close()

    @distributed_trace()
    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Get user by id
        TODO: cache user data
        :param user_id:
        :return:
        """
        try:
            user = await (
                self._session.select(
                    SysUser.id,
                    SysUser.email,
                    SysUser.username,
                    SysUser.display_name,
                    SysUser.hash_password,
                    SysUser.password_salt,
                    SysUser.is_superuser,
                    SysUser.is_active,
                    SysUser.otp_active,
                    SysUser.otp_secret,
                    SysUser.last_login_at
                )
                .where(SysUser.id == user_id)
                .fetchrow(as_model=User)
            )
        except Exception as e:
            raise e
        else:
            return user
        finally:
            await self._session.close()

    @distributed_trace()
    async def update_last_login(self, user_id: UUID, last_login: datetime):
        """
        Update last login
        :param user_id:
        :param last_login:
        :return:
        """
        last_login_at = last_login.strftime("%Y-%m-%d %H:%M:%S")
        try:
            await (
                self._session.update(SysUser)
                .values(last_login_at=last_login_at)
                .where(SysUser.id == user_id)
                .execute()
            )
        except Exception as e:
            await self._session.rollback()
            raise e
        else:
            await self._session.commit()
        finally:
            await self._session.close()

    @distributed_trace()
    async def reset_otp_secret(self, user_id: UUID):
        """
        Reset otp secret
        :param user_id:
        :return:
        """
        try:
            await (
                self._session.update(SysUser)
                .values(
                    otp_active=False,
                    otp_secret=None
                )
                .where(SysUser.id == user_id)
                .execute()
            )
        except Exception as e:
            await self._session.rollback()
            raise e
        else:
            await self._session.commit()
        finally:
            await self._session.close()

    @distributed_trace()
    async def update_otp_secret(self, user_id: UUID, otp_secret: str):
        """
        Update otp secret
        :param user_id:
        :param otp_secret:
        :return:
        """
        try:
            await (
                self._session.update(SysUser)
                .values(
                    otp_active=True,
                    otp_secret=otp_secret
                )
                .where(SysUser.id == user_id)
                .execute()
            )
        except Exception as e:
            await self._session.rollback()
            raise e
        else:
            await self._session.commit()
        finally:
            await self._session.close()
