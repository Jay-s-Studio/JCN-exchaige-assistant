"""
Contains all the messages used in the telegram bot.
"""
from pydantic import BaseModel, Field, ConfigDict
from collections import defaultdict
from typing import Dict, Optional, Type, List, Union

from telegram import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
    InlineKeyboardButton,
)
from telegram._utils.types import ReplyMarkup
from telegram.constants import ParseMode

from app.libs.consts.enums import Language


class Message(BaseModel):
    """Message"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    text: str
    parse_mode: Optional[ParseMode] = Field(default=None)
    reply_markup: Optional[ReplyMarkup] = None


class MarkupButton(BaseModel):
    """MarkupButton"""
    text: str
    callback_data: Optional[str]


class MessagesBase:
    """MessagesBase"""
    message: Dict[Language, str] = defaultdict(Dict[Language, str])
    parse_mode: Optional[ParseMode] = None
    reply_markup_obj: Optional[Type[ReplyMarkup]] = None
    markup_buttons: Optional[Dict[Language, List[MarkupButton]]] = None

    def __getitem__(self, language: Language):
        """
        get item
        :param language:
        :return:
        """
        return self.message[language]

    @classmethod
    def generate_markup(cls, language: Language, *args, **kwargs) -> Optional[ReplyMarkup]:
        """
        generate_markup
        :param language:
        :param args:
        :param kwargs:
        :return:
        """
        if cls.reply_markup_obj == InlineKeyboardMarkup:
            buttons = []
            for markup_button in cls.markup_buttons.get(language):
                buttons.append(
                    InlineKeyboardButton(
                        text=markup_button.text,
                        callback_data=markup_button.callback_data.format(*args, **kwargs)
                    )
                )
            return InlineKeyboardMarkup(inline_keyboard=[buttons])

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
            parse_mode=cls.parse_mode,
            reply_markup=cls.generate_markup(language=language, *args, **kwargs)
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


class CartInfoMessage(MessagesBase):
    """CartInfoMessage"""
    message = {
        Language.ZH_TW: (
            "請確認您的訂單資訊 \n\n"
            "● 支付貨幣/方式: `{payment_currency}`\n"
            "● 換匯貨幣: `{exchange_currency}`\n"
            "● 匯率: `{exchange_rate}`\n"
            "● 總金額: `{total_price}`\n\n"
            "若資訊正確，請點擊「確認下單」，將會提供您支付資訊。\n"
            "若還需增加金額，請繼續輸入文字。\n"
            "謝謝！\n\n"
            "訂單成立且收到支付資訊後，請於 1 小時內完成支付，否則訂單將自動取消。"
        ),
        Language.EN_US: (
            "Please confirm your order information \n\n"
            "● Payment currency/method: `{payment_currency}`\n"
            "● Exchange currency: `{exchange_currency}`\n"
            "● Exchange rate: `{exchange_rate}`\n"
            "● Total amount: `{total_price}`\n\n"
            "If the content is correct and the order is confirmed, please click 'Confirm order', and you will be provided with payment account information.\n"
            "If you need to add more amount, please continue to enter text.\n"
            "Thanks!\n\n"
            "After the order is established and payment information is received, please complete the payment within 1 hour, "
            "otherwise the order will be automatically cancelled."
        ),
    }
    parse_mode = ParseMode.MARKDOWN_V2
    reply_markup_obj = InlineKeyboardMarkup
    markup_buttons = {
        Language.ZH_TW: [
            MarkupButton(text="確認下單", callback_data="ORDER_CONFIRM {cart_id}"),
        ],
        Language.EN_US: [
            MarkupButton(text="Confirm order", callback_data="ORDER_CONFIRM {cart_id}"),
        ]
    }


class CartCurrencyMismatchMessage(MessagesBase):
    """CartCurrencyMismatchMessage"""
    message = {
        Language.ZH_TW: "抱歉，您的訂單貨幣不匹配",
        Language.EN_US: "Sorry, your order currency does not match",
    }
    parse_mode = ParseMode.MARKDOWN_V2


class OrderConfirmationMessage(MessagesBase):
    """OrderConfirmationMessage"""
    message = {
        Language.ZH_TW: "您的訂單已確認，馬上為您提供支付資訊，請稍等，謝謝！",
        Language.EN_US: "Your order has been confirmed, payment information will be provided to you soon, please wait, thank you!",
    }
    parse_mode = ParseMode.MARKDOWN_V2


class OrderInProgressMessage(MessagesBase):
    """OrderInProgressMessage"""
    message = {
        Language.ZH_TW: "您有一個訂單正在進行中，請完成支付後再下單",
        Language.EN_US: "You have an order in progress, please place an order after completing the payment",
    }
    parse_mode = ParseMode.MARKDOWN_V2


class OrderInfoNotFoundMessage(MessagesBase):
    """OrderInfoNotFoundMessage"""
    message = {
        Language.ZH_TW: "抱歉，找不到訂單信息，請確認有成功下單",
        Language.EN_US: "Sorry, order information not found, please make sure you have successfully placed an order",
    }
    parse_mode = ParseMode.MARKDOWN_V2


class ConfirmPaymentMessage(MessagesBase):
    """ConfirmPaymentMessage"""
    message = {
        Language.ZH_TW: "為您查收中，請稍等",
        Language.EN_US: "Checking for you, please wait",
    }
    parse_mode = ParseMode.MARKDOWN_V2


class ConfirmPayMessage(MessagesBase):
    """ConfirmPayMessage"""
    message = {
        Language.ZH_TW: "您的訂單已支付成功",
        Language.EN_US: "Your order has been successfully paid",
    }
    parse_mode = ParseMode.MARKDOWN_V2
