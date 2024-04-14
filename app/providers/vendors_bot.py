"""
VendorsBotProvider
"""
from app.clients.vendors_bot import VendorsBotClient
from app.libs.decorators.sentry_tracer import distributed_trace
from app.schemas.vendors_bot import GetPaymentAccount, CheckReceipt, ConfirmPayment, VendorBotBroadcast, VendorBotMessage


class VendorsBotProvider:
    """VendorsBotProvider"""

    def __init__(self):
        self._client = VendorsBotClient()

    @distributed_trace()
    async def broadcast(self, payload: VendorBotBroadcast) -> VendorBotMessage:
        """
        broadcast
        :param payload:
        :return:
        """
        result = await self._client.broadcast(payload=payload)
        return VendorBotMessage(**result)

    @distributed_trace()
    async def payment_account(self, payload: GetPaymentAccount):
        """
        payment account
        :param payload:
        :return:
        """
        await self._client.payment_account(payload=payload)

    @distributed_trace()
    async def hurry_payment_account(self, payload: GetPaymentAccount):
        """
        hurry payment account
        :param payload:
        :return:
        """
        await self._client.hurry_payment_account(payload=payload)

    @distributed_trace()
    async def check_receipt(self, payload: CheckReceipt):
        """
        check receipt
        :param payload:
        :return:
        """
        await self._client.check_receipt(payload=payload)

    @distributed_trace()
    async def confirm_payment(self, payload: ConfirmPayment):
        """
        confirm payment
        :param payload:
        :return:
        """
        await self._client.confirm_payment(payload=payload)
