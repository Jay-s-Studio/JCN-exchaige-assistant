"""
Serializers for Exchange Rate API
"""
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ExchangeRate(BaseModel):
    """
    Exchange Rate
    """
    currency_id: UUID = Field(title="Currency ID")
    buy_rate: Optional[float] = Field(default=None, title="Buy Rate", ge=0)
    sell_rate: Optional[float] = Field(default=None, title="Sell Rate", ge=0)


class ExchangeRateResponse(BaseModel):
    """
    Exchange Rate Response
    """
    exchange_rates: List[ExchangeRate] = Field(title="Exchange Rate")


class GroupExchangeRate(BaseModel):
    """
    Group Exchange Rate
    """
    group_id: int = Field(title="Group ID")
    exchange_rates: List[ExchangeRate] = Field(title="Exchange Rate")


class UpdateExchangeRate(BaseModel):
    """
    Update Exchange Rate
    """
    group_id: int = Field(title="Group ID")
    currency_rates: List[ExchangeRate] = Field(title="Exchange Rate")
