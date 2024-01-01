"""
Serializer for handing fee API
"""
from pydantic import BaseModel


class HandingFee(BaseModel):
    """
    HandingFee
    """
    buying_fee: float
    selling_fee: float
