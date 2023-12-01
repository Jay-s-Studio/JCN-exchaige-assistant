"""
Currency provider fixtures
"""
import pytest

from app.containers import Container
from app.providers import CurrencyProvider


@pytest.fixture
def currency_provider() -> CurrencyProvider:
    """Currency provider fixture"""
    container = Container()
    return container.currency_provider()
