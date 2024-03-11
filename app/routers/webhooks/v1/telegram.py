"""
Telegram Router
"""
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
    :param request:
    :return:
    """
    json_data = await request.json()
    update = Update.de_json(data=json_data, bot=application.bot)
    await application.update_queue.put(update)
    return Response()
