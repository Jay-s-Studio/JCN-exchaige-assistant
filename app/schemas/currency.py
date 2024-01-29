"""
Serializers for currency API
"""
from typing import Optional
from uuid import UUID

from pydantic import field_validator, Field

from app.libs.consts.enums import CurrencyType
from app.schemas.mixins import UUIDBaseModel


class Currency(UUIDBaseModel):
    """
    Currency
    """
    symbol: str
    type: CurrencyType = Field(default=CurrencyType.GENERAL)
    path: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    sequence: Optional[float] = Field(default=None)
    parent_id: Optional[UUID] = Field(default=None)

    @field_validator("symbol", mode="before")
    def validate_name(cls, value: str):
        """
        Validate name
        :param value:
        :return:
        """
        return value.upper()
