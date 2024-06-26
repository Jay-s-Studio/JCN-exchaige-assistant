"""
Serializer for handling fee API
"""
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, ConfigDict

from app.libs.consts.enums import CalculationType
from app.libs.shared import validator
from app.schemas.mixins import UUIDBaseModel


class HandlingFeeConfigBase(UUIDBaseModel):
    """
    HandlingFeeConfigBase
    """
    name: str = Field(title="Name", description="Name of the fee")
    is_global: bool = Field(default=False, title="Is Global", description="Is the fee global")
    description: Optional[str] = Field(default=None, title="Description", description="Description of the fee")

    @field_validator("name")
    def check_empty(cls, value):
        """

        :param value:
        :return:
        """
        if validator.is_empty(value):
            raise ValueError("Required.")
        return value


class HandlingFeeConfigItem(BaseModel):
    """
    HandlingFeeConfigItem
    """
    model_config = ConfigDict(use_enum_values=True)
    currency_id: UUID = Field(title="Currency ID", description="Currency ID")
    buy_calculation_type: CalculationType = Field(title="Buy Calculation Type", description="Buy Calculation Type")
    buy_value: float = Field(title="Buy Value", description="Buy Value")
    sell_calculation_type: CalculationType = Field(title="Sell Calculation Type", description="Sell Calculation Type")
    sell_value: float = Field(title="Sell Value", description="Sell Value")


class HandlingFeeConfig(HandlingFeeConfigBase):
    """
    HandlingFeeConfig
    """
    items: List[HandlingFeeConfigItem] = Field(title="Items", description="Items of the fee")


class HandlingFeeConfigPage(BaseModel):
    """
    HandlingFeeConfigPage
    """
    total: int = Field(title="Total", description="Total count")
    configs: List[HandlingFeeConfigBase] = Field(title="Configs", description="Configs of the page")


class HandlingFeeConfigs(BaseModel):
    """
    HandlingFeeConfigs
    """
    values: List[HandlingFeeConfigBase] = Field(title="Values", description="Values of the configs")
