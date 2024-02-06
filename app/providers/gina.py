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
from app.schemas.gina import GinaHeaders, GinaPayload, GinaMessage, GinaResponse
from . import FileProvider
from ..schemas.files import TelegramFile


class GinaProvider:
    """GinaProvider"""

    def __init__(
        self,
        file_provider: FileProvider
    ):
        self._client = GinaClient()
        self._file_provider = file_provider

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
                message = GinaMessage(text=update.message.text)
            else:
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
                image_url = urljoin(base=settings.BASE_URL, url=f"/api/v1/files/{file.file_unique_id}")
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
