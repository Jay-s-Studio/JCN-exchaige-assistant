"""
Contains all the messages used in the telegram bot.
"""
from collections import defaultdict
from typing import Dict

from app.libs.consts.enums import Language


class MessagesBase:
    """MessagesBase"""
    message: Dict[Language, str] = defaultdict(Dict[Language, str])

    def __getitem__(self, language: Language):
        """
        get item
        :param language:
        :return:
        """
        return self.message[language]

    @classmethod
    def format(cls, language: Language, *args, **kwargs):
        """
        format
        :param language:
        :param args:
        :param kwargs:
        :return:
        """
        return cls.message[language].format(*args, **kwargs)


class ExchangeRateMessage(MessagesBase):
    message = {
        Language.ZH_TW: "當前 `{payment_currency}-{exchange_currency}` 匯率為 `{price}`",
        Language.EN_US: "The current `{payment_currency}-{exchange_currency}` exchange rate is `{price}`",
    }
