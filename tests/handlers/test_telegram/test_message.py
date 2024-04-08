"""
Test message handler.
"""
import pytest

from app.handlers import TelegramMessageHandler
from app.libs.consts.enums import BotType
from app.serializers.v1.telegram import TelegramBroadcast


@pytest.mark.asyncio
async def test_broadcast_message(telegram_message_handler: TelegramMessageHandler):
    """
    Test broadcast_message
    :param telegram_message_handler:
    :return:
    """
    broadcast = TelegramBroadcast(
        message="Test broadcast message",
        type=BotType.VENDORS,
        chat_id_list=[
            -4100117630,
            -1002003483337
        ]
    )
    await telegram_message_handler.broadcast_message(model=broadcast)
