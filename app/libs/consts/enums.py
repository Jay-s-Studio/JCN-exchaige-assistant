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


class GinaIntention(StrEnum):
    """GinaIntention
    swap
    payment check
    exchange rate
    human customer service
    get account
    receipt
    cancel order
    hurry
    """
    SWAP = "swap"
    PAYMENT_CHECK = "payment check"
    EXCHANGE_RATE = "exchange rate"
    HUMAN_CUSTOMER_SERVICE = "human customer service"
    GET_ACCOUNT = "get account"
    RECEIPT = "receipt"
    CANCEL_ORDER = "cancel order"
    HURRY = "hurry"


class GinaAction(StrEnum):
    """GinaAction
    swap_crypto
    swap_legal
    payment check
    exchange rate
    human customer service
    get account
    receipt
    cancel order
    hurry
    """
    SWAP_CRYPTO = "swap_crypto"
    SWAP_LEGAL = "swap_legal"
    PAYMENT_CHECK = "payment check"
    EXCHANGE_RATE = "exchange rate"
    HUMAN_CUSTOMER_SERVICE = "human customer service"
    GET_ACCOUNT = "get account"
    RECEIPT = "receipt"
    CANCEL_ORDER = "cancel order"
    HURRY = "hurry"
