"""
MessagesController
"""
import asyncio
from dataclasses import dataclass
from typing import List, Optional, Callable

from telegram import Update
from telegram.constants import ParseMode

from app.libs.consts import messages
from app.libs.consts.enums import GinaAction, CurrencySymbol
from app.libs.consts.messages import Message
from app.libs.decorators.sentry_tracer import distributed_trace
from app.providers import ExchangeRateProvider, TelegramAccountProvider
from app.schemas.exchange_rate import CurrentExchangeRate
from app.schemas.gina import GinaResponse
from app.serializers.v1.exchange_rate import GroupExchangeRate


@dataclass
class FormatOptions:
    """FormatOptions"""
    customer_service: bool = True


class MessagesController:
    """MessagesController"""

    def __init__(
        self,
        telegram_account_provider: TelegramAccountProvider,
        exchange_rate_provider: ExchangeRateProvider,
    ):
        self._telegram_account_provider = telegram_account_provider
        self._exchange_rate_provider = exchange_rate_provider

    @distributed_trace()
    async def on_exchange_rate(self, update: Update, gina_resp: GinaResponse) -> Message:
        """
        on exchange rate
        :param update:
        :param gina_resp:
        :return:
        """
        match gina_resp.action:
            case GinaAction.EXCHANGE_RATE:
                message = await self.exchange_rate(update=update, gina_resp=gina_resp)
            case GinaAction.EXCHANGE_RATE_MAIN_TOKEN:
                message = await self.exchange_rate(update=update, gina_resp=gina_resp, get_default=True)
            case _:
                message = Message(text=gina_resp.reply)
        return message

    @distributed_trace()
    async def on_swap(self, update: Update, gina_resp: GinaResponse) -> Message:
        """
        on swap
        :param update:
        :param gina_resp:
        :return:
        """
        match gina_resp.action:
            case GinaAction.SWAP:
                message = Message(text=gina_resp.reply)
            case GinaAction.SWAP_CRYPTO:
                message = Message(text=gina_resp.reply)
            case GinaAction.SWAP_LEGAL:
                message = Message(text=gina_resp.reply)
            case _:
                message = Message(text=gina_resp.reply)
        return message

    @distributed_trace()
    async def on_human_customer_service(self, update: Update, gina_resp: GinaResponse) -> Message:
        """
        on human customer service
        :param update:
        :param gina_resp:
        :return:
        """
        return Message(
            text=await self.format_message(
                message=gina_resp.reply,
                group_id=update.effective_chat.id,
                options=FormatOptions()
            ),
            parse_mode=ParseMode.HTML
        )

    @distributed_trace()
    async def on_fallback(self, update: Update, gina_resp: GinaResponse) -> Message:
        """
        on fallback
        :param update:
        :param gina_resp:
        :return:
        """
        return Message(text=gina_resp.reply)

    async def format_message(
        self,
        message: str,
        group_id: int,
        options: FormatOptions = None
    ) -> str:
        """
        format message
        :param message:
        :param group_id:
        :param options:
        :return:
        """
        if not options:
            return message
        if options.customer_service:
            message = await self._format_customer_service(message=message, group_id=group_id)
        return message

    async def _format_customer_service(self, message: str, group_id: int) -> str:
        """

        :param message:
        :param group_id:
        :return:
        """
        # group = await self._telegram_account_provider.get_chat_group(chat_id=group_id)
        # if not group.custom_info.customer_service:
        #     return message
        # user = User(
        #     id=group.custom_info.customer_service.id,
        #     first_name=group.custom_info.customer_service.first_name,
        #     is_bot=group.custom_info.customer_service.is_bot,
        #     last_name=group.custom_info.customer_service.last_name,
        #     username=group.custom_info.customer_service.username,
        #     language_code=group.custom_info.customer_service.language_code,
        #     is_premium=group.custom_info.customer_service.is_premium
        # )
        # customer_service = user.mention_html(name=f"@{user.username}")
        # message = message.replace("#CUSTOMER_SERVICE#", customer_service)
        return message

    @distributed_trace()
    async def exchange_rate(self, update: Update, gina_resp: GinaResponse, get_default: bool = False) -> Message:
        """
        exchange rate
        :param update:
        :param gina_resp:
        :param get_default:
        :return:
        """
        await update.effective_message.reply_text(text=gina_resp.reply)
        exchange_rate_list = await self._exchange_rate_provider.get_all_exchange_rate()
        if get_default:
            group = await self._telegram_account_provider.get_chat_group(group_id=update.effective_chat.id)
            if not group.currency_symbol:
                return messages.DefaultCurrencyNotFoundMessage.format(language=gina_resp.language)
            payment_currency = group.currency_symbol
            exchange_currency = CurrencySymbol.USDT.value
        else:
            payment_currency = gina_resp.payment_currency.upper()
            exchange_currency = gina_resp.exchange_currency.upper()
        if payment_currency != "USDT":
            exchange_rate = self.get_lowest_buying_exchange_rate(
                currency=payment_currency,
                exchange_rate_list=exchange_rate_list
            )
            price = exchange_rate.buy
        else:
            exchange_rate = self.get_highest_selling_exchange_rate(
                currency=exchange_currency,
                exchange_rate_list=exchange_rate_list
            )
            price = exchange_rate.sell
        await asyncio.sleep(1.5)
        return messages.ExchangeRateMessage.format(
            language=gina_resp.language,
            payment_currency=payment_currency,
            exchange_currency=exchange_currency,
            price=price
        )

    @staticmethod
    def _get_optimal_exchange_rate(
        currency: str,
        exchange_rate_list: List[GroupExchangeRate],
        compare_func: Callable
    ) -> Optional[CurrentExchangeRate]:
        """
        Internal function to get the optimal exchange rate based on a comparison function.
        :param currency: The currency to find the exchange rate for.
        :param exchange_rate_list: A list of GroupExchangeRate objects.
        :param compare_func: A function to compare two exchange rates.
        :return: The optimal CurrentExchangeRate object or None.
        """
        optimal_rate = None
        for group_rate in exchange_rate_list:
            for exchange_rate in group_rate.exchange_rates:
                if exchange_rate.currency != currency:
                    continue
                if optimal_rate is None:
                    optimal_rate = CurrentExchangeRate(
                        group_id=group_rate.group_id,
                        currency=currency,
                        buy=exchange_rate.buy_rate,
                        sell=exchange_rate.sell_rate
                    )
                    continue
                if compare_func(exchange_rate, optimal_rate):
                    optimal_rate = CurrentExchangeRate(
                        group_id=group_rate.group_id,
                        currency=currency,
                        buy=exchange_rate.buy_rate,
                        sell=exchange_rate.sell_rate
                    )
        return optimal_rate

    def get_lowest_buying_exchange_rate(
        self,
        currency: str,
        exchange_rate_list: List[GroupExchangeRate]
    ) -> Optional[CurrentExchangeRate]:
        """
        Get the exchange rate with the lowest buying rate for a given currency.
        :param currency: The currency to find the exchange rate for.
        :param exchange_rate_list: A list of GroupExchangeRate objects.
        :return: The CurrentExchangeRate object with the lowest buying rate or None.
        """
        return self._get_optimal_exchange_rate(
            currency, exchange_rate_list,
            lambda rate, current: rate.buy_rate < current.buy
        )

    def get_highest_selling_exchange_rate(
        self,
        currency: str,
        exchange_rate_list: List[GroupExchangeRate]
    ) -> Optional[CurrentExchangeRate]:
        """
        Get the exchange rate with the highest selling rate for a given currency.
        :param currency: The currency to find the exchange rate for.
        :param exchange_rate_list: A list of GroupExchangeRate objects.
        :return: The CurrentExchangeRate object with the highest selling rate or None.
        """
        return self._get_optimal_exchange_rate(
            currency, exchange_rate_list,
            lambda rate, current: rate.sell_rate > current.sell
        )
