"""
Schema for price
"""
from pydantic import BaseModel


class PriceInfo(BaseModel):
    """
    Price Info
    """
    vendor_name: str
    vendor_id: int
    original_rate: float
    price: float
