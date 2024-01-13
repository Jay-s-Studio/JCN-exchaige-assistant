"""
Serializer for handing fee API
"""
from typing import Optional
from pydantic import BaseModel, Field


class HandingFee(BaseModel):
    """
    HandingFee
    """
    buying_fee: Optional[float] = Field(default=None)
    selling_fee: Optional[float] = Field(default=None)
