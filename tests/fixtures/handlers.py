"""
Fixtures for handlers
"""
import pytest

from app.handlers import (
    AuthHandler,
    CurrencyHandler,
    ExchangeRateHandler,
    TelegramAccountHandler,
    TelegramMessageHandler,
    HandlingFeeHandler,
    UserHandler,
)
from app.containers import Container


@pytest.fixture
def auth_handler() -> AuthHandler:
    """
    auth_handler
    :return:
    """
    return Container.auth_handler()


@pytest.fixture
def currency_handler() -> CurrencyHandler:
    """
    currency_handler
    :return:
    """
    return Container.currency_handler()


@pytest.fixture
def exchange_rate_handler() -> ExchangeRateHandler:
    """
    exchange_rate_handler
    :return:
    """
    return Container.exchange_rate_handler()


@pytest.fixture
def telegram_account_handler() -> TelegramAccountHandler:
    """
    telegram_account_handler
    :return:
    """
    return Container.telegram_account_handler()


@pytest.fixture
def telegram_message_handler() -> TelegramMessageHandler:
    """
    telegram_message_handler
    :return:
    """
    return Container.telegram_message_handler()


@pytest.fixture
def handling_fee_handler() -> HandlingFeeHandler:
    """
    handling_fee_handler
    :return:
    """
    return Container.handling_fee_handler()


@pytest.fixture
def user_handler() -> UserHandler:
    """
    user_handler
    :return:
    """
    return Container.user_handler()
