"""
Constants for Redis keys
"""
from app.config import settings


def get_redis_key(key: str) -> str:
    """
    Get Redis key
    :param key:
    :return:
    """
    return f"{settings.APP_NAME}:{key}"


def get_user_key(user_id: str) -> str:
    """
    Get the user key
    :param user_id:
    :return:
    """
    return get_redis_key(f"user:{user_id}")


def get_user_access_token_key(user_id: str) -> str:
    """
    Get the user access token key
    :param user_id:
    :return:
    """
    return get_redis_key(f"user:access_token:{user_id}")
