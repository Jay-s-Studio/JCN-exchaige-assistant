"""
TelegramBotMessagesHandler
"""
from telegram import Update

from app.config import settings
from app.context import CustomContext
from app.controllers import MessagesController
from app.libs.consts.enums import GinaIntention
from app.libs.database import RedisPool
from app.libs.decorators.sentry_tracer import distributed_trace
from app.libs.logger import logger
from app.providers import TelegramAccountProvider, GinaProvider
from app.serializers.v1.telegram import TelegramAccount, TelegramChatGroup
from .base import TelegramBotBaseHandler


class TelegramBotMessagesHandler(TelegramBotBaseHandler):
    """TelegramBotMessagesHandler"""

    def __init__(
        self,
        redis: RedisPool,
        telegram_account_provider: TelegramAccountProvider,
        gina_provider: GinaProvider,
        messages_controller: MessagesController
    ):
        super().__init__(
            redis=redis,
            telegram_account_provider=telegram_account_provider
        )
        self._gina_provider = gina_provider
        self._messages_controller = messages_controller

    @staticmethod
    def redis_name(name: str):
        """

        :return:
        """
        return f"{settings.APP_NAME}:{name}"

    @distributed_trace()
    async def receive_message(self, update: Update, context: CustomContext) -> None:
        """
        receive message
        controller
        :param update:
        :param context:
        :return:
        """
        await self.setup_account_info(
            account=TelegramAccount(**update.effective_user.to_dict()),
            chat_group=TelegramChatGroup(
                **update.effective_chat.to_dict(),
                in_group=True,
                bot_type=settings.TELEGRAM_BOT_TYPE
            )
        )
        await update.effective_chat.send_chat_action("typing")
        result = await self._gina_provider.telegram_messages(update=update)
        if not result:
            await update.effective_message.reply_text(text="Sorry, There is something wrong. Please try again later. 🙇🏼‍")
            return

        # [Flow] exchange rate process
        match result.intention:
            case GinaIntention.EXCHANGE_RATE:
                message = await self._messages_controller.on_exchange_rate(update=update, gina_resp=result)
            case GinaIntention.SWAP:
                message = await self._messages_controller.on_swap(update=update, gina_resp=result)
            case GinaIntention.HUMAN_CUSTOMER_SERVICE:
                message = await self._messages_controller.on_human_customer_service(update=update, gina_resp=result)
            case _:
                message = await self._messages_controller.on_fallback(update=update, gina_resp=result)

        logger.info(f"Intentions: {result.intention}, Actions: {result.action}")
        logger.info(f"Gina response: {result}")
        await update.effective_message.reply_text(
            text=message.text,
            parse_mode=message.parse_mode
        )
