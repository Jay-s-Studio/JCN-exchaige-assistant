"""
Serializers for Telegram Group Type API
"""
from typing import List

from pydantic import BaseModel, Field

from app.schemas.mixins import UUIDBaseModel


class TelegramGroupType(UUIDBaseModel):
    """TelegramGroupType"""
    name: str = Field(description="Name", max_length=16)


class TelegramGroupTypes(BaseModel):
    """TelegramGroupTypes"""
    values: List[TelegramGroupType] = Field(description="Values")
