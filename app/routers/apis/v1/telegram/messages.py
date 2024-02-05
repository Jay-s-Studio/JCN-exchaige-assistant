"""
Telegram Messages API Router
"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from app.containers import Container
from app.handlers.telegram import TelegramMessageHandler
from app.libs.depends import check_all_authenticators, DEFAULT_RATE_LIMITERS
from app.route_classes import LogRoute
from app.serializers.v1.telegram import TelegramBroadcast, PaymentAccount

router = APIRouter(
    dependencies=[
        Depends(check_all_authenticators),
        *DEFAULT_RATE_LIMITERS
    ],
    route_class=LogRoute
)


@router.post(
    path="/broadcast",
    status_code=status.HTTP_200_OK
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


@router.post(
    path="/payment_account",
    status_code=status.HTTP_200_OK
)
@inject
async def receive_payment_account(
    model: PaymentAccount,
    telegram_message_handler: TelegramMessageHandler = Depends(Provide[Container.telegram_message_handler])
):
    """

    :param model:
    :param telegram_message_handler:
    :return:
    """
    await telegram_message_handler.receive_payment_account(model=model)
    return {"message": "success"}
