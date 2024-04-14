"""
Top level package for providers.
"""
from .account import TelegramAccountProvider
from .telegram import TelegramGroupTypeProvider
from .currency import CurrencyProvider
from .exchange_rate import ExchangeRateProvider
from .files import FileProvider
from .gina import GinaProvider
from .handling_fee import HandlingFeeProvider
from .message import MessageProvider
from .order import OrderProvider
from .price import PriceProvider
from .user import UserProvider
from .vendors_bot import VendorsBotProvider

__all__ = [
    # account package
    "TelegramAccountProvider",
    # telegram package
    "TelegramGroupTypeProvider",
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
    # message
    "MessageProvider",
    # order
    "OrderProvider",
    # price
    "PriceProvider",
    # user
    "UserProvider",
    # vendors_bot
    "VendorsBotProvider",
]
