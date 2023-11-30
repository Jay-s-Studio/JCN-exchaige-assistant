"""
Container
"""
from dependency_injector import containers, providers

from app.libs.database import redis_pool
from app.providers import TelegramAccountProvider


# pylint: disable=too-few-public-methods,c-extension-no-member
class Container(containers.DeclarativeContainer):
    """Container"""

    wiring_config = containers.WiringConfiguration(
        modules=[],
        packages=["app.handlers", "app.routers"],
    )

    # [database]
    redis_pool = providers.Resource(redis_pool)

    # [providers]
    telegram_account_provider = providers.Factory(
        TelegramAccountProvider,
        redis=redis_pool
    )

    # [handlers]

