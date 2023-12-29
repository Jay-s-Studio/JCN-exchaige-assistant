"""
TelegramAccountHandler
"""
from telegram import Bot

from app.libs.consts.enums import BotType
from app.providers import TelegramAccountProvider


class TelegramAccountHandler:
    """TelegramAccountHandler"""

    def __init__(self, bot: Bot, telegram_account_provider: TelegramAccountProvider):
        self._bot = bot
        self._telegram_account_provider = telegram_account_provider

    async def get_vendors(self):
        """get_vendors"""
        accounts = await self._telegram_account_provider.get_all_chat_group()
        return {
            "vendors": list(filter(lambda x: x.bot_type == BotType.VENDORS, accounts))
        }
