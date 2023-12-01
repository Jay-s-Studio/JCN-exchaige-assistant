"""
Serializers for currency API
"""
from typing import List

from pydantic import BaseModel, field_validator


class Currency(BaseModel):
    """
    Currency
    """
    name: str
    description: str
    sequence: int

    @field_validator("name", mode="before")
    def validate_name(cls, value: str):
        """
        Validate name
        :param value:
        :return:
        """
        return value.upper()


class CurrencyList(BaseModel):
    """
    Currency List
    """
    currencies: List[Currency]
