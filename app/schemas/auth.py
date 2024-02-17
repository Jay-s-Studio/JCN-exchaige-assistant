"""
Models for auth
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_serializer, ConfigDict

from app.libs.consts.enums import TokenScope


class JWTPayload(BaseModel):
    """
    JWT Payload
    """
    model_config = ConfigDict(use_enum_values=True)
    iss: str
    uid: UUID
    sub: str
    name: str
    iat: datetime
    exp: datetime
    scope: TokenScope

    @field_serializer("uid")
    def serialize_uuid(self, value: UUID, _info) -> str:
        """

        :param value:
        :param _info:
        :return:
        """
        return str(value)
