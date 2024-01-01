"""
Fixtures for providers
"""
import pytest

from app.containers import Container
from app.providers import CurrencyProvider, HandingFeeProvider, UserProvider


@pytest.fixture
def currency_provider() -> CurrencyProvider:
    """Currency provider fixture"""
    container = Container()
    return container.currency_provider()


@pytest.fixture
def handing_fee_provider() -> HandingFeeProvider:
    """Handing fee provider fixture"""
    container = Container()
    return container.handing_fee_provider()


@pytest.fixture
def user_provider() -> UserProvider:
    """User provider fixture"""
    container = Container()
    return container.user_provider()
