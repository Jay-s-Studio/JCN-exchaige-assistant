"""
Model for Exchange Rate
"""
from pydantic import BaseModel


class CurrentExchangeRate(BaseModel):
    """
    Model for Exchange Rate
    """
    group_id: str
    currency: str
    buy: float
    sell: float
