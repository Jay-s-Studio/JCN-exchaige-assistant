"""
Serializer for handing fee API
"""
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field

from app.libs.consts.enums import CalculationType, OperationType
from app.schemas.mixins import UUIDBaseModel


class HandingFeeConfigBase(UUIDBaseModel):
    """
    HandingFeeConfigBase
    """
    name: str = Field(title="Name", description="Name of the fee", max_length=32)
    is_global: bool = Field(default=False, title="Is Global", description="Is the fee global")
    description: Optional[str] = Field(default=None, title="Description", description="Description of the fee")


class HandingFeeConfigItem(BaseModel):
    """
    HandingFeeConfigItem
    """
    currency_id: UUID = Field(title="Currency ID", description="Currency ID")
    buy_calculation_type: CalculationType = Field(title="Buy Calculation Type", description="Buy Calculation Type")
    buy_value: float = Field(title="Buy Value", description="Buy Value")
    sell_calculation_type: CalculationType = Field(title="Sell Calculation Type", description="Sell Calculation Type")
    sell_value: float = Field(title="Sell Value", description="Sell Value")


class HandingFeeConfig(HandingFeeConfigBase):
    """
    HandingFeeConfig
    """
    items: List[HandingFeeConfigItem] = Field(title="Items", description="Items of the fee")


class HandingFeeConfigPage(BaseModel):
    """
    HandingFeeConfigPage
    """
    total: int = Field(title="Total", description="Total count")
    configs: List[HandingFeeConfigBase] = Field(title="Items", description="Items of the page")
