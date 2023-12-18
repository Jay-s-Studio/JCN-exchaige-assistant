"""
Serializers for Exchange Rate API
"""
from typing import List

from pydantic import BaseModel, Field


class ExchangeRate(BaseModel):
    """
    Exchange Rate
    """
    currency: str = Field(title="Currency", max_length=255)
    buy_rate: float = Field(title="Buy Rate", gt=0)
    sell_rate: float = Field(title="Sell Rate", gt=0)


class UpdateExchangeRate(BaseModel):
    """
    Update Exchange Rate
    """
    group_id: str = Field(title="Group ID", max_length=255)
    currency_rates: List[ExchangeRate] = Field(title="Exchange Rate")
