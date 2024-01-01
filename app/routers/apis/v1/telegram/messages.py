"""
Telegram Messages API Router
"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from app.containers import Container
from app.handlers.telegram import TelegramMessageHandler
from app.libs.auth.bearer_jwt import BearerJWTAuth
from app.routing import LogRouting
from app.serializers.v1.telegram import TelegramBroadcast

router = APIRouter(dependencies=[Depends(BearerJWTAuth())], route_class=LogRouting)


@router.post(
    path="/broadcast"
)
@inject
async def broadcast(
    model: TelegramBroadcast,
    telegram_message_handler: TelegramMessageHandler = Depends(Provide[Container.telegram_message_handler])
):
    """

    :param model:
    :param telegram_message_handler:
    :return:
    """
    return await telegram_message_handler.broadcast_message(model=model)