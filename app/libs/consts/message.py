"""
Contains all the messages used in the telegram bot.
"""
from pydantic import BaseModel, Field
from collections import defaultdict
from typing import Dict, Optional

from telegram.constants import ParseMode

from app.libs.consts.enums import Language


class Message(BaseModel):
    text: str
    parse_mode: Optional[ParseMode] = Field(default=None)


class MessagesBase:
    """MessagesBase"""
    message: Dict[Language, str] = defaultdict(Dict[Language, str])
    parse_mode: Optional[ParseMode] = None

    def __getitem__(self, language: Language):
        """
        get item
        :param language:
        :return:
        """
        return self.message[language]

    @classmethod
    def format(cls, language: Language, *args, **kwargs) -> Message:
        """
        format
        :param language:
        :param args:
        :param kwargs:
        :return:
        """
        return Message(
            text=cls.message[language].format(*args, **kwargs),
            parse_mode=cls.parse_mode
        )


class ExchangeRateMessage(MessagesBase):
    message = {
        Language.ZH_TW: "當前 `{payment_currency}-{exchange_currency}` 匯率為 `{price}`",
        Language.EN_US: "The current `{payment_currency}-{exchange_currency}` exchange rate is `{price}`",
    }
    parse_mode = ParseMode.MARKDOWN_V2
