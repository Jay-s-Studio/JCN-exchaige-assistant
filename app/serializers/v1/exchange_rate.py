"""
Serializers for Exchange Rate API
"""
from typing import List, Optional

from pydantic import BaseModel, Field


class ExchangeRate(BaseModel):
    """
    Exchange Rate
    """
    currency: str = Field(title="Currency", max_length=255)
    buy_rate: Optional[float] = Field(default=None, title="Buy Rate", ge=0)
    sell_rate: Optional[float] = Field(default=None, title="Sell Rate", ge=0)


class GroupExchangeRate(BaseModel):
    """
    Group Exchange Rate
    """
    group_id: str = Field(title="Group ID", max_length=255)
    exchange_rates: List[ExchangeRate] = Field(title="Exchange Rate")


class UpdateExchangeRate(BaseModel):
    """
    Update Exchange Rate
    """
    group_id: str = Field(title="Group ID", max_length=255)
    currency_rates: List[ExchangeRate] = Field(title="Exchange Rate")
