"""
Enums for the application
"""
from enum import StrEnum, IntEnum


class ExpireTime(IntEnum):
    """ExpireTime"""
    ONE_HOUR = 60 * 60
    ONE_DAY = 60 * 60 * 24
    ONE_WEEK = 60 * 60 * 24 * 7
    ONE_MONTH = 60 * 60 * 24 * 30
    ONE_YEAR = 60 * 60 * 24 * 365


class BotType(StrEnum):
    """BotType"""
    CUSTOMER = "customer"
    VENDORS = "vendors"
