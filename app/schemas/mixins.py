"""
Model for Mixins
"""
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer


class UUIDBaseModel(BaseModel):
    """
    UUID Base Model
    """
    id: UUID = Field(default_factory=UUID)

    @field_serializer("id")
    def serialize_uuid(self, value: UUID, _info) -> str:
        """

        :param value:
        :param _info:
        :return:
        """
        return str(value)
