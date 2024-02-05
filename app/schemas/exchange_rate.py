"""
Model for Exchange Rate
"""
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class OptimalExchangeRate(BaseModel):
    """
    OptimalExchangeRate
    """
    group_id: int
    currency_id: UUID
    currency: str
    buy_rate: Optional[float]
    sell_rate: Optional[float]
