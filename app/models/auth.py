"""
Models for auth
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_serializer


class JWTPayload(BaseModel):
    """
    JWT Payload
    """
    iss: str
    uid: UUID
    sub: str
    name: str
    iat: datetime
    exp: datetime

    @field_serializer("uid")
    def serialize_uuid(self, value: UUID, _info) -> str:
        """

        :param value:
        :param _info:
        :return:
        """
        return str(value)
