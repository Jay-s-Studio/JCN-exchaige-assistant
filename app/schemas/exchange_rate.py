"""
Model for Exchange Rate
"""
from typing import Optional

from pydantic import BaseModel


class CurrentExchangeRate(BaseModel):
    """
    Model for Exchange Rate
    """
    group_id: str
    currency: str
    buy: Optional[float]
    sell: Optional[float]
