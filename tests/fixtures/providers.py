"""
Fixtures for providers
"""
import pytest

from app.containers import Container
from app.providers import (
    CurrencyProvider,
    ExchangeRateProvider,
    HandlingFeeProvider,
    OrderProvider,
    UserProvider,
    TelegramAccountProvider,
    PriceProvider
)


@pytest.fixture
def currency_provider() -> CurrencyProvider:
    """Currency provider fixture"""
    container = Container()
    return container.currency_provider()


@pytest.fixture
def exchange_rate_provider() -> ExchangeRateProvider:
    """Exchange rate provider fixture"""
    container = Container()
    return container.exchange_rate_provider()


@pytest.fixture
def handling_fee_provider() -> HandlingFeeProvider:
    """Handing fee provider fixture"""
    container = Container()
    return container.handling_fee_provider()


@pytest.fixture
def order_provider() -> OrderProvider:
    """Order provider fixture"""
    container = Container()
    return container.order_provider()


@pytest.fixture
def user_provider() -> UserProvider:
    """User provider fixture"""
    container = Container()
    return container.user_provider()


@pytest.fixture
def telegram_account_provider() -> TelegramAccountProvider:
    """Telegram account provider fixture"""
    container = Container()
    return container.telegram_account_provider()


@pytest.fixture
def price_provider() -> PriceProvider:
    """Price provider fixture"""
    container = Container()
    return container.price_provider()
