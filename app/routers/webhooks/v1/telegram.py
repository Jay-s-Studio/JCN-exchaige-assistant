"""
Telegram Router
"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Request, Response
from telegram import Update

from app.bot import application
from app.containers import Container
from app.handlers.telegram import TelegramHandler
from app.serializers.v1.telegram import TelegramBroadcast

router = APIRouter()


@router.post(
    path="/telegram",
)
async def telegram(request: Request) -> Response:
    """Handle incoming Telegram updates by putting them into the `update_queue`"""
    update = Update.de_json(data=await request.json(), bot=application.bot)
    await application.update_queue.put(update)
    return Response()
