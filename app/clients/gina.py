"""
GinaClient
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
from app.schemas.gina import GinaHeaders, GinaPayload


class GinaClient:
    """GinaClient"""

    def __init__(self):
        self._url = settings.GINA_URL
        self._api_key = settings.GINA_API_KEY

    @distributed_trace(inject_span=True)
    async def messages(
        self,
        headers: GinaHeaders,
        payload: GinaPayload,
        *,
        _span: Span
    ) -> Optional[dict]:
        """

        :param headers:
        :param payload:
        :param _span:
        :return:
        """
        span_data = defaultdict()
        url = urljoin(base=self._url, url="/chatai_api/v1/messages")
        span_data["headers"] = headers.model_dump(by_alias=True)
        span_data["payload"] = payload.model_dump(exclude_none=True)
        try:
            resp = await (
                http_client.create(url=url)
                .add_headers(headers.model_dump(by_alias=True))
                .add_header(name="x-api-key", value=self._api_key)
                .add_json(payload.model_dump(exclude_none=True))
                .apost()
            )
            resp.raise_for_status()
            span_data["status_code"] = resp.status_code
            span_data["response"] = resp.json()
            return resp.json()
        except HTTPStatusError as e:
            span_data["status_code"] = e.response.status_code
            span_data["response"] = e.response.text
            logger.exception(e)
            return None
        finally:
            for key, value in span_data.items():
                _span.set_data(key, value)
