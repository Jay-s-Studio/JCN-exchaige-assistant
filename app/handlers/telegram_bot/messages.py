"""
TelegramBotMessagesHandler
"""
from typing import cast

from telegram import Update
from telegram.constants import ParseMode

from app.config import settings
from app.context import CustomContext
from app.controllers import MessagesController
from app.libs.consts.enums import GinaIntention
from app.libs.database import RedisPool
from app.libs.decorators.sentry_tracer import distributed_trace
from app.libs.logger import logger
from app.providers import TelegramAccountProvider, GinaProvider, FileProvider
from app.schemas.files import TelegramFile
from app.serializers.v1.telegram import TelegramAccount, TelegramChatGroup
from .base import TelegramBotBaseHandler
from ...libs.consts.messages import Message


class TelegramBotMessagesHandler(TelegramBotBaseHandler):
    """TelegramBotMessagesHandler"""

    def __init__(
        self,
        redis: RedisPool,
        telegram_account_provider: TelegramAccountProvider,
        file_provider: FileProvider,
        gina_provider: GinaProvider,
        messages_controller: MessagesController
    ):
        super().__init__(
            redis=redis,
            telegram_account_provider=telegram_account_provider
        )
        self._file_provider = file_provider
        self._gina_provider = gina_provider
        self._messages_controller = messages_controller

    @staticmethod
    def redis_name(name: str):
        """

        :return:
        """
        return f"{settings.APP_NAME}:{name}"

    @distributed_trace()
    async def reply_message(self, update: Update, message: Message) -> None:
        """
        reply message
        :param update:
        :param message:
        :return:
        """
        match message.parse_mode:
            case ParseMode.MARKDOWN:
                await update.effective_message.reply_markdown(
                    text=message.text,
                    reply_markup=message.reply_markup
                )
            case ParseMode.MARKDOWN_V2:
                await update.effective_message.reply_markdown_v2(
                    text=message.text,
                    reply_markup=message.reply_markup
                )
            case ParseMode.HTML:
                await update.effective_message.reply_html(
                    text=message.text,
                    reply_markup=message.reply_markup
                )
            case _:
                await update.effective_message.reply_text(
                    text=message.text,
                    reply_markup=message.reply_markup
                )

    @distributed_trace()
    async def pre_process_files(self, update: Update, context: CustomContext) -> TelegramFile:
        """
        pre process files
        :param update:
        :param context:
        :return:
        """
        if update.message.document:
            file = await update.message.document.get_file()
            file_name = update.message.document.file_name
            content_type = update.message.document.mime_type
            telegram_file = TelegramFile(
                file_unique_id=file.file_unique_id,
                file=file,
                file_name=file_name,
                content_type=content_type
            )
        else:
            file = await update.message.photo[-1].get_file()
            file_name = file.file_path.split("/")[-1]
            content_type = "image/jpg"
            telegram_file = TelegramFile(
                file_unique_id=file.file_unique_id,
                file=file,
                file_name=file_name,
                content_type=content_type
            )
        await self._file_provider.set_file(file=telegram_file)
        return telegram_file

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
        telegram_file = None
        if update.message.document or update.message.photo:
            telegram_file = await self.pre_process_files(update=update, context=context)

        result = await self._gina_provider.telegram_messages(update=update, telegram_file=telegram_file)
        if not result:
            await update.effective_message.reply_text(text="Sorry, There is something wrong. Please try again later. 🙇🏼‍")
            return

        # [Flow] exchange rate process
        try:
            match result.intention:
                case GinaIntention.EXCHANGE_RATE:
                    message = await self._messages_controller.on_exchange_rate(update=update, gina_resp=result)
                case GinaIntention.SWAP:
                    message = await self._messages_controller.on_swap(update=update, gina_resp=result)
                case GinaIntention.HUMAN_CUSTOMER_SERVICE:
                    message = await self._messages_controller.on_human_customer_service(update=update, gina_resp=result)
                case GinaIntention.GET_ACCOUNT:
                    message = await self._messages_controller.on_get_account(update=update, gina_resp=result)
                case GinaIntention.RECEIPT:
                    message = await self._messages_controller.on_confirm_payment(update=update, gina_resp=result)
                case GinaIntention.PAYMENT_CHECK:
                    message = await self._messages_controller.on_payment_check(update=update, gina_resp=result)
                case GinaIntention.CANCEL_ORDER:
                    message = await self._messages_controller.on_cancel_order(update=update, gina_resp=result)
                case GinaIntention.HURRY:
                    message = await self._messages_controller.on_hurry(update=update, gina_resp=result)
                case _:
                    message = await self._messages_controller.on_fallback(update=update, gina_resp=result)
        except Exception as e:
            logger.exception(e)
            message = await self._messages_controller.on_exception(update=update, gina_resp=result)

        await self.reply_message(update=update, message=message)

    @distributed_trace()
    async def order_confirmation(self, update: Update, context: CustomContext) -> None:
        """
        order confirmation
        :param update:
        :param context:
        :return:
        """
        await update.effective_chat.send_chat_action("typing")
        callback_query = update.callback_query
        _, cart_id = cast(str, callback_query.data).split()
        await update.effective_message.edit_text(
            text=update.effective_message.text_markdown_v2,
            parse_mode=ParseMode.MARKDOWN_V2
        )

        message = await self._messages_controller.on_order_confirmation(update=update, cart_id=cart_id)
        await self.reply_message(update=update, message=message)
