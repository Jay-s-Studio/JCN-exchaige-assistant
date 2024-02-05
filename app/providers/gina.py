"""
GinaProvider
"""
from typing import Optional

from sentry_sdk.tracing import Span
from telegram import Update

from app.clients.gina import GinaClient
from app.libs.decorators.sentry_tracer import distributed_trace
from app.libs.logger import logger
from app.schemas.gina import GinaHeaders, GinaPayload, GinaMessage, GinaResponse


class GinaProvider:
    """GinaProvider"""

    def __init__(self):
        self._client = GinaClient()

    @distributed_trace(inject_span=True)
    async def telegram_messages(
        self,
        update: Update,
        *,
        _span: Span = None
    ) -> Optional[GinaResponse]:
        """
        telegram messages
        :param update:
        :param _span:
        :return:
        """
        try:
            headers = GinaHeaders(
                chat_group_id=str(update.effective_chat.id),
                chat_user_id=str(update.effective_user.id),
                chat_platform="telegram",
                chat_mode="group"
            )
            if update.message.text:
                message = GinaMessage(
                    text=update.message.text
                )
                payload = GinaPayload(
                    messages=[message]
                )
            else:
                if update.message.document:
                    file = await update.message.document.get_file()
                    file_name = update.message.document.file_name
                    content_type = update.message.document.mime_type
                else:
                    file = await update.message.photo[-1].get_file()
                    file_name = file.file_path.split("/")[-1]
                    content_type = "image/jpg"
                data = await file.download_as_bytearray()
                payload = GinaPayload(
                    image=(file_name, data, content_type)
                )
            data = await self._client.messages(headers=headers, payload=payload)
            if not data:
                return None
            return GinaResponse(**data)
        except Exception as e:
            _span.set_status("error")
            _span.set_data("error", str(e))
            logger.exception(e)
            return None
