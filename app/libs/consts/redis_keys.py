"""
Constants for Redis keys
"""
from uuid import UUID

from app.config import settings


def get_redis_key(key: str) -> str:
    """
    Get Redis key
    :param key:
    :return:
    """
    return f"{settings.APP_NAME}:{key}"


def get_user_key(user_id: UUID) -> str:
    """
    Get the user key
    :param user_id:
    :return:
    """
    return get_redis_key(f"user:{str(user_id)}")


def get_user_access_token_key(user_id: UUID) -> str:
    """
    Get the user access token key
    :param user_id:
    :return:
    """
    return get_redis_key(f"user:access_token:{str(user_id)}")


def get_user_otp_secret_key(user_id: UUID) -> str:
    """
    Get the user OTP secret key
    :param user_id:
    :return:
    """
    return get_redis_key(f"user:otp_secret:{str(user_id)}")
