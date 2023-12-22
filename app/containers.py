"""
Container
"""
from dependency_injector import containers, providers

from app.libs.database import RedisPool
from app.providers import (
    TelegramAccountProvider,
    CurrencyProvider,
    ExchangeRateProvider,
    UserProvider
)
from app.handlers.currency import CurrencyHandler
from app.handlers.exchange_rate import ExchangeRateHandler
from app.handlers.user import UserHandler


# pylint: disable=too-few-public-methods,c-extension-no-member
class Container(containers.DeclarativeContainer):
    """Container"""

    wiring_config = containers.WiringConfiguration(
        modules=[],
        packages=["app.handlers", "app.routers"],
    )

    # [database]
    redis_pool = providers.Singleton(RedisPool)

    # [providers]
    telegram_account_provider = providers.Factory(
        TelegramAccountProvider,
        redis=redis_pool
    )
    currency_provider = providers.Factory(
        CurrencyProvider,
        redis=redis_pool
    )
    exchange_rate_provider = providers.Factory(
        ExchangeRateProvider,
        redis=redis_pool
    )
    user_provider = providers.Factory(
        UserProvider,
        redis=redis_pool
    )

    # [handlers]
    currency_handler = providers.Factory(
        CurrencyHandler,
        currency_provider=currency_provider
    )
    exchange_rate_handler = providers.Factory(
        ExchangeRateHandler,
        exchange_rate_provider=exchange_rate_provider
    )
    user_handler = providers.Factory(
        UserHandler,
        user_provider=user_provider
    )
