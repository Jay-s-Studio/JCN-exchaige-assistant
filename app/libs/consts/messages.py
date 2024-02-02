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
    """ExchangeRateMessage"""
    message = {
        Language.ZH_TW: "當前 `{payment_currency}-{exchange_currency}` 匯率為 `{price}`",
        Language.EN_US: "The current `{payment_currency}-{exchange_currency}` exchange rate is `{price}`",
    }
    parse_mode = ParseMode.MARKDOWN_V2


class ExchangeRateErrorMessage(MessagesBase):
    """ExchangeRateErrorMessage"""
    message = {
        Language.ZH_TW: "抱歉，我們無法為您提供 `{payment_currency}-{exchange_currency}` 的匯率",
        Language.EN_US: "Sorry, we are unable to provide you with the `{payment_currency}-{exchange_currency}` exchange rate",
    }
    parse_mode = ParseMode.MARKDOWN_V2


class DefaultCurrencyNotFoundMessage(MessagesBase):
    """DefaultCurrencyNotFoundMessage"""
    message = {
        Language.ZH_TW: "請先設置默認貨幣",
        Language.EN_US: "Please set the default currency first",
    }
    parse_mode = ParseMode.MARKDOWN_V2
