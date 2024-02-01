"""
Models for user
"""
from datetime import datetime
from typing import Optional

from pydantic import Field

from app.schemas.mixins import UUIDBaseModel


class User(UUIDBaseModel):
    """
    User
    """
    email: str
    username: str
    display_name: str
    hash_password: str
    password_salt: str
    is_superuser: bool = Field(default=False)
    is_active: bool = Field(default=False)
    gac: Optional[str] = Field(default=None)
    last_login_at: Optional[datetime] = None
