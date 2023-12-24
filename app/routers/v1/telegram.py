"""
Telegram Router
"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from app.containers import Container
from app.handlers.telegram import TelegramHandler
from app.serializers.v1.telegram import TelegramBroadcast

router = APIRouter()


@router.post(
    path="/broadcast"
)
@inject
async def broadcast(
    model: TelegramBroadcast,
    telegram_handler: TelegramHandler = Depends(Provide[Container.telegram_handler])
):
    """

    :param model:
    :param telegram_handler:
    :return:
    """
    return await telegram_handler.broadcast_message(model)
