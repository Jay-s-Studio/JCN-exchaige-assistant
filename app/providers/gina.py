"""
GinaProvider
"""
from typing import Optional
from urllib.parse import urljoin

from sentry_sdk.tracing import Span
from telegram import Update

from app.clients.gina import GinaClient
from app.config import settings
from app.libs.decorators.sentry_tracer import distributed_trace
from app.libs.logger import logger
from app.schemas.files import TelegramFile
from app.schemas.gina import GinaHeaders, GinaPayload, GinaMessage, GinaResponse


class GinaProvider:
    """GinaProvider"""

    def __init__(self):
        self._client = GinaClient()

    @distributed_trace(inject_span=True)
    async def telegram_messages(
        self,
        update: Update,
        telegram_file: Optional[TelegramFile] = None,
        *,
        _span: Span = None
    ) -> Optional[GinaResponse]:
        """
        telegram messages
        :param update:
        :param telegram_file:
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
                message = GinaMessage(text=update.message.text)
            else:
                image_url = urljoin(
                    base=settings.BASE_URL,
                    url=f"/api/v1/files/{telegram_file.file_unique_id}/{telegram_file.file_name}"
                )
                message = GinaMessage(image=image_url)
            payload = GinaPayload(
                messages=[message]
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
