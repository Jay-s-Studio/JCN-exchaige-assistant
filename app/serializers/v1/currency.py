"""
Serializers for currency API
"""
from typing import Optional, List
from uuid import UUID

from pydantic import field_validator, Field, BaseModel

from app.schemas.mixins import UUIDBaseModel


class CurrencyInfo(UUIDBaseModel):
    """
    Currency
    """
    symbol: str
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


class CurrencyNode(UUIDBaseModel):
    """
    Currency Node
    """
    symbol: str
    description: Optional[str] = Field(default=None)
    sequence: Optional[float] = Field(default=None)
    parent_id: Optional[UUID] = Field(default=None)
    children: Optional[List["CurrencyNode"]] = Field(default=None)


class CurrencyTree(BaseModel):
    """
    Currency Tree
    """
    nodes: List[CurrencyNode]


class Currencies(BaseModel):
    """
    Currencies
    """
    currencies: List[CurrencyInfo]
