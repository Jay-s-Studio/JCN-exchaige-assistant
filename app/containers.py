"""
Container
"""
from dependency_injector import containers, providers
from telegram import Bot

from app.config import settings
from app.controllers import MessagesController
from app.handlers import (
    AuthHandler,
    CurrencyHandler,
    ExchangeRateHandler,
    FileHandler,
    HandlingFeeHandler,
    TelegramAccountHandler,
    TelegramMessageHandler,
    TelegramGroupTypeHandler,
    TelegramBotMessagesHandler,
    OrderHandler,
    UserHandler,
)
from app.libs.database import RedisPool, Session
from app.providers import (
    TelegramAccountProvider,
    TelegramGroupTypeProvider,
    CurrencyProvider,
    ExchangeRateProvider,
    FileProvider,
    GinaProvider,
    HandlingFeeProvider,
    MessageProvider,
    OrderProvider,
    PriceProvider,
    UserProvider,
    VendorsBotProvider
)


# pylint: disable=too-few-public-methods,c-extension-no-member
class Container(containers.DeclarativeContainer):
    """Container"""

    wiring_config = containers.WiringConfiguration(
        modules=[],
        packages=["app.bots", "app.handlers", "app.routers"],
    )

    # [bot]
    bot = providers.Resource(
        Bot,
        token=settings.TELEGRAM_BOT_TOKEN
    )

    # [database]
    aio_session = providers.Singleton(Session)
    redis_pool = providers.Singleton(RedisPool)

    # [providers]
    telegram_account_provider = providers.Factory(
        TelegramAccountProvider,
        session=aio_session,
        redis=redis_pool
    )
    telegram_group_type_provider = providers.Factory(
        TelegramGroupTypeProvider,
        session=aio_session
    )
    currency_provider = providers.Factory(
        CurrencyProvider,
        session=aio_session,
        redis=redis_pool
    )
    exchange_rate_provider = providers.Factory(
        ExchangeRateProvider,
        session=aio_session,
        redis=redis_pool
    )
    file_provider = providers.Factory(
        FileProvider,
        bot=bot,
        redis=redis_pool
    )
    gina_provider = providers.Factory(GinaProvider)
    handling_fee_provider = providers.Factory(
        HandlingFeeProvider,
        session=aio_session,
        redis=redis_pool
    )
    message_provider = providers.Factory(
        MessageProvider,
        session=aio_session
    )
    order_provider = providers.Factory(
        OrderProvider,
        session=aio_session,
        redis=redis_pool
    )
    price_provider = providers.Factory(
        PriceProvider,
        exchange_rate_provider=exchange_rate_provider,
        handling_fee_provider=handling_fee_provider
    )
    user_provider = providers.Factory(
        UserProvider,
        session=aio_session,
        redis=redis_pool
    )
    vendors_bot_provider = providers.Factory(VendorsBotProvider)

    # [controllers]
    messages_controller = providers.Factory(
        MessagesController,
        telegram_account_provider=telegram_account_provider,
        price_provider=price_provider,
        order_provider=order_provider,
        vendors_bot_provider=vendors_bot_provider
    )

    # [handlers]
    auth_handler = providers.Factory(AuthHandler)
    currency_handler = providers.Factory(
        CurrencyHandler,
        currency_provider=currency_provider
    )
    exchange_rate_handler = providers.Factory(
        ExchangeRateHandler,
        exchange_rate_provider=exchange_rate_provider
    )
    file_handler = providers.Factory(
        FileHandler,
        file_provider=file_provider
    )
    handling_fee_handler = providers.Factory(
        HandlingFeeHandler,
        handling_fee_provider=handling_fee_provider
    )
    telegram_account_handler = providers.Factory(
        TelegramAccountHandler,
        bot=bot,
        telegram_account_provider=telegram_account_provider,
        group_type_provider=telegram_group_type_provider
    )
    telegram_message_handler = providers.Factory(
        TelegramMessageHandler,
        bot=bot,
        telegram_account_provider=telegram_account_provider,
        order_provider=order_provider,
        price_provider=price_provider,
        message_provider=message_provider,
        vendors_bot_provider=vendors_bot_provider
    )
    telegram_group_type_handler = providers.Factory(
        TelegramGroupTypeHandler,
        group_type_provider=telegram_group_type_provider
    )
    telegram_bot_messages_handler = providers.Factory(
        TelegramBotMessagesHandler,
        redis=redis_pool,
        telegram_account_provider=telegram_account_provider,
        file_provider=file_provider,
        gina_provider=gina_provider,
        messages_controller=messages_controller
    )
    order_handler = providers.Factory(
        OrderHandler,
        order_provider=order_provider
    )
    user_handler = providers.Factory(
        UserHandler,
        redis=redis_pool,
        auth_handler=auth_handler,
        user_provider=user_provider
    )
