"""
MessagesController
"""
import asyncio
from dataclasses import dataclass
from typing import List, Optional, Callable

from telegram import Update, User
from telegram.constants import ParseMode

from app.libs.consts.enums import GinaIntention
from app.libs.consts.message import ExchangeRateMessage, Message
from app.libs.decorators.sentry_tracer import distributed_trace
from app.libs.logger import logger
from app.schemas.exchange_rate import CurrentExchangeRate
from app.schemas.gina import GinaResponse
from app.providers import GinaProvider, ExchangeRateProvider, TelegramAccountProvider
from app.serializers.v1.exchange_rate import GroupExchangeRate


@dataclass
class FormatOptions:
    """FormatOptions"""
    customer_service: bool = True


class MessagesController:
    """MessagesController"""

    def __init__(
        self,
        gina_provider: GinaProvider,
        telegram_account_provider: TelegramAccountProvider,
        exchange_rate_provider: ExchangeRateProvider,
    ):
        self._gina_provider = gina_provider
        self._telegram_account_provider = telegram_account_provider
        self._exchange_rate_provider = exchange_rate_provider

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
    async def receive_message(self, update: Update) -> None:
        """
        receive message
        :param update:
        :return:
        """
        await update.effective_chat.send_chat_action("typing")
        result = await self._gina_provider.telegram_messages(update=update)
        if not result:
            await update.effective_message.reply_text(text="Sorry, There is something wrong. Please try again later. 🙇🏼‍")
            return
        match result.intention:
            case GinaIntention.EXCHANGE_RATE:
                message = await self.exchange_rate(update=update, gina_resp=result)
            case GinaIntention.SWAP:
                message = Message(text=result.reply)
            case GinaIntention.HUMAN_CUSTOMER_SERVICE:
                message = Message(
                    text=await self.format_message(
                        message=result.reply,
                        group_id=update.effective_chat.id,
                        options=FormatOptions()
                    ),
                    parse_mode=ParseMode.HTML
                )
            case _:
                message = Message(text=result.reply)
        logger.info(f"Gina response: {result}")
        await update.effective_message.reply_text(
            text=message.text,
            parse_mode=message.parse_mode
        )

    @distributed_trace()
    async def exchange_rate(self, update: Update, gina_resp: GinaResponse) -> Message:
        """
        exchange rate
        :param update:
        :param gina_resp:
        :return:
        """
        await update.effective_message.reply_text(text=gina_resp.reply)
        exchange_rate_list = await self._exchange_rate_provider.get_all_exchange_rate()
        if gina_resp.payment_currency.upper() != "USDT":
            exchange_rate = self.get_lowest_buying_exchange_rate(
                currency=gina_resp.payment_currency,
                exchange_rate_list=exchange_rate_list
            )
            price = exchange_rate.buy
        else:
            exchange_rate = self.get_highest_selling_exchange_rate(
                currency=gina_resp.exchange_currency,
                exchange_rate_list=exchange_rate_list
            )
            price = exchange_rate.sell
        await asyncio.sleep(1.5)
        return ExchangeRateMessage.format(
            language=gina_resp.language,
            payment_currency=gina_resp.payment_currency,
            exchange_currency=gina_resp.exchange_currency,
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
