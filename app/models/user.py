"""
Models for user
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_serializer


class User(BaseModel):
    """
    User
    """
    id: UUID
    username: str
    hash_password: str
    password_salt: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    @field_serializer("id")
    def serialize_uuid(self, value: UUID, _info):
        """

        :param value:
        :param _info:
        :return:
        """
        return value.hex
