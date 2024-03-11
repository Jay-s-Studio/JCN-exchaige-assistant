"""
Enums for the application
"""
from enum import StrEnum, IntEnum


class StatusBase(StrEnum):
    """StatusBase"""
    ENABLED = "enabled"
    DISABLED = "disabled"


class TokenScope(StrEnum):
    """JWTTokenScope"""
    ACCESS = "access"
    TWO_FACTOR_AUTH = "2fa"


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


class PaymentAccountStatus(StrEnum):
    """PaymentAccountStatus"""
    PREPARING = "preparing"
    OUT_OF_STOCK = "out_of_stock"


class Language(StrEnum):
    """Language"""
    EN_US = "en-us"
    ZH_TW = "zh-tw"
    ZH_CN = "zh-cn"


class CurrencySymbol(StrEnum):
    """CurrencySymbol"""
    USDT = "USDT"
    PHP = "PHP"
    JPY = "JPY"
    INR = "INR"
    KRW = "KRW"
    THB = "THB"
    MYR = "MYR"
    USD = "USD"
    CAD = "CAD"
    HKD = "HKD"
    SGD = "SGD"
    VND = "VND"
    AUD = "AUD"
    AED = "AED"
    MMK = "MMK"
    BDT = "BDT"


class CurrencyType(StrEnum):
    """CurrencyType"""
    GENERAL = "general"
    PAYMENT = "payment"


class GinaIntention(StrEnum):
    """GinaIntention"""
    SWAP = "swap"
    EXCHANGE_RATE = "exchange rate"
    HUMAN_CUSTOMER_SERVICE = "human customer service"
    GET_ACCOUNT = "get account"
    RECEIPT = "receipt"
    PAYMENT_CHECK = "payment check"
    CANCEL_ORDER = "cancel order"
    HURRY = "hurry"


class GinaAction(StrEnum):
    """GinaAction"""
    SWAP = "swap"
    SWAP_CRYPTO = "swap_crypto"
    SWAP_LEGAL = "swap_legal"
    PAYMENT_CHECK = "payment check"
    EXCHANGE_RATE = "exchange rate"
    EXCHANGE_RATE_MAIN_TOKEN = "exchange_rate_main_token"
    HUMAN_CUSTOMER_SERVICE = "human customer service"
    GET_ACCOUNT = "get account"
    RECEIPT = "receipt"
    CANCEL_ORDER = "cancel order"
    HURRY = "hurry"


class OperationType(StrEnum):
    """OperationType"""
    BUY = "buy"
    SELL = "sell"


class CalculationType(StrEnum):
    """CalculationType"""
    ADDITION = "addition"
    SUBTRACTION = "subtraction"
    MULTIPLICATION = "multiplication"
    DIVISION = "division"


class CartStatus(StrEnum):
    """CartStatus"""
    PENDING = "pending"
    CONFIRMED = "confirmed"


class OrderStatus(StrEnum):
    """OrderStatus"""
    WAIT_FOR_PAYMENT_ACCOUNT = "wait_for_payment_account"
    WAIT_FOR_PAYMENT = "wait_for_payment"
    EXPIRE = "expire"
    WAIT_FOR_CONFIRMATION = "wait_for_confirmation"
    DONE = "done"
    CANCELLED = "cancelled"
