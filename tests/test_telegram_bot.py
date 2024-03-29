"""
Test the telegram bot
"""
import pytest
from telegram import Bot

from app.containers import Container

chat_id = 1259597115


@pytest.mark.asyncio
async def test_send_message():
    bot: Bot = Container.bot()
    await bot.send_message(chat_id=chat_id, text="Hello, World!")
