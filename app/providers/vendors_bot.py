"""
VendorsBotProvider
"""
from app.clients.vendors_bot import VendorsBotClient
from app.libs.decorators.sentry_tracer import distributed_trace
from app.schemas.vendors_bot import PaymentAccount


class VendorsBotProvider:
    """VendorsBotProvider"""

    def __init__(self):
        self._client = VendorsBotClient()

    @distributed_trace()
    async def payment_account(self, payload: PaymentAccount):
        """
        payment account
        :param payload:
        :return:
        """
        await self._client.payment_account(payload=payload)
