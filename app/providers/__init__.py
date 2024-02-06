"""
Top level package for providers.
"""
from .account import TelegramAccountProvider
from .currency import CurrencyProvider
from .exchange_rate import ExchangeRateProvider
from .files import FileProvider
from .gina import GinaProvider
from .handling_fee import HandlingFeeProvider
from .order import OrderProvider
from .user import UserProvider
from .vendors_bot import VendorsBotProvider

__all__ = [
    # account package
    "TelegramAccountProvider",
    # currency
    "CurrencyProvider",
    # exchange_rate
    "ExchangeRateProvider",
    # files
    "FileProvider",
    # gina
    "GinaProvider",
    # handling_fee
    "HandlingFeeProvider",
    # order
    "OrderProvider",
    # user
    "UserProvider",
    # vendors_bot
    "VendorsBotProvider",
]
