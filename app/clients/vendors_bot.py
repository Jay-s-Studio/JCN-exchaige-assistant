"""
VendorsBotClient
"""
from collections import defaultdict
from typing import Optional
from urllib.parse import urljoin

from httpx import HTTPStatusError
from sentry_sdk.tracing import Span

from app.config import settings
from app.libs.decorators.sentry_tracer import distributed_trace
from app.libs.http_client import http_client
from app.libs.logger import logger
from app.schemas.vendors_bot import PaymentAccount


class VendorsBotClient:
    """VendorsBotClient"""

    def __init__(self):
        self._url = settings.JCN_VENDORS_BOT_URL
        self._version = "v1"

    def _get_resource_url(self, resource: str, path: str):
        """

        :param path:
        :return:
        """
        assert resource, "resource can't be None"
        assert path.startswith("/"), "A path prefix must start with '/'"
        return urljoin(base=self._url, url=f"/api/{self._version}/{resource}{path}")

    @distributed_trace(inject_span=True)
    async def payment_account(
        self,
        payload: PaymentAccount,
        *,
        _span: Span
    ):
        """

        :param payload:
        :param _span:
        :return:
        """
        span_data = defaultdict()
        url = self._get_resource_url(resource="telegram/messages", path="/payment_account")
        span_data["payload"] = payload.model_dump(exclude_none=True)
        try:
            resp = await (
                http_client.create(url=url)
                .add_json(payload.model_dump(exclude_none=True))
                .apost()
            )
            resp.raise_for_status()
            span_data["status_code"] = resp.status_code
            span_data["response"] = resp.json()
        except HTTPStatusError as e:
            span_data["status_code"] = e.response.status_code
            span_data["response"] = e.response.text
            logger.exception(e)
            return None
        finally:
            for key, value in span_data.items():
                _span.set_data(key, value)
