"""
MessagesController
"""
from typing import List, Optional, Callable

from telegram import Update

from app.libs.consts.enums import GinaIntention
from app.models.exchange_rate import CurrentExchangeRate
from app.providers import GinaProvider, ExchangeRateProvider
from app.serializers.v1.exchange_rate import GroupExchangeRate


class MessagesController:
    """MessagesController"""

    def __init__(
        self,
        gina_provider: GinaProvider,
        exchange_rate_provider: ExchangeRateProvider,
    ):
        self._gina_provider = gina_provider
        self._exchange_rate_provider = exchange_rate_provider

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
        reply_message = result.reply
        match result.intention:
            case GinaIntention.EXCHANGE_RATE:
                exchange_rate_list = await self._exchange_rate_provider.get_all_exchange_rate()
                if result.payment_currency.upper() != "USDT":
                    exchange_rate = self.get_lowest_buying_exchange_rate(
                        currency=result.payment_currency,
                        exchange_rate_list=exchange_rate_list
                    )
                else:
                    exchange_rate = self.get_highest_selling_exchange_rate(
                        currency=result.exchange_currency,
                        exchange_rate_list=exchange_rate_list
                    )
                print(exchange_rate)
            case _:
                pass

        await update.effective_message.reply_text(text=reply_message)

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
            for rate in group_rate.exchange_rates:
                if rate.currency != currency:
                    continue
                if optimal_rate is None:
                    optimal_rate = CurrentExchangeRate(
                        group_id=group_rate.group_id,
                        currency=currency,
                        buy=rate.buy_rate,
                        sell=rate.sell_rate
                    )
                    continue
                if compare_func(rate, optimal_rate):
                    optimal_rate = CurrentExchangeRate(
                        group_id=group_rate.group_id,
                        currency=currency,
                        buy=rate.buy_rate,
                        sell=rate.sell_rate
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
