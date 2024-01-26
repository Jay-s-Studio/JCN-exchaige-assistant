"""
Models for user
"""
from datetime import datetime
from typing import Optional

from app.schemas.mixins import UUIDBaseModel


class User(UUIDBaseModel):
    """
    User
    """
    username: str
    display_name: str
    hash_password: str
    password_salt: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None
