"""
Telegram Router
"""
import sentry_sdk
from fastapi import APIRouter, Request, Response
from telegram import Update

from app.bot import application

router = APIRouter()


@router.post(
    path="/telegram",
)
async def telegram(request: Request) -> Response:
    """
    Handle incoming Telegram updates by putting them into the `update_queue`
    TODO: inject current span into the context, because the job in the queue is executed in a different thread
    :param request:
    :return:
    """
    update = Update.de_json(data=await request.json(), bot=application.bot)
    # span = sentry_sdk.get_current_span()
    await application.update_queue.put(update)
    return Response()
