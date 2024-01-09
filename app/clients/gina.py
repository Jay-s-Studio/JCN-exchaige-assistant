"""
GinaClient
"""
from typing import Optional
from urllib.parse import urljoin

from httpx import HTTPStatusError

from app.config import settings
from app.libs.http_client import http_client
from app.libs.logger import logger
from app.models.gina import GinaHeaders, GinaPayload


class GinaClient:
    """GinaClient"""

    def __init__(self):
        self._url = settings.GINA_URL
        self._api_key = settings.GINA_API_KEY

    async def messages(self, headers: GinaHeaders, payload: GinaPayload) -> Optional[dict]:
        """

        :param headers:
        :param payload:
        :return:
        """
        url = urljoin(base=self._url, url="/chatai_api/v1/messages")
        try:
            resp = await (
                http_client.create(url=url)
                .add_headers(headers.model_dump(by_alias=True))
                .add_header(name="x-api-key", value=self._api_key)
                .add_json(payload.model_dump(exclude_none=True))
                .apost()
            )
            resp.raise_for_status()
            return resp.json()
        except HTTPStatusError as e:
            logger.exception(e)
            return None
