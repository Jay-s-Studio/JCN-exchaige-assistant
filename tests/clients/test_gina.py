"""
Test the GINA client.
"""
import pytest

from app.clients.gina import GinaClient
from app.schemas.gina import GinaHeaders, GinaMessage, GinaPayload


@pytest.mark.asyncio
async def test_message():
    """
    Test the GINA client.
    :return:
    """
    client = GinaClient()
    headers = GinaHeaders(
        chat_group_id="-1002050270240",
        chat_user_id="1259597115",
        chat_platform="telegram",
        chat_mode="group",
        os="linux",
    )
    message = GinaMessage(
        text="請問目前CAD換U匯率?"
    )
    payload = GinaPayload(
        messages=[message]
    )
    resp = await client.messages(headers=headers, payload=payload)
    assert resp is not None
