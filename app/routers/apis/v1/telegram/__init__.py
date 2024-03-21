"""
Top level router for telegram API
"""
from fastapi import APIRouter

from .account import router as account_router
from .messages import router as message_router
from .group_type import router as group_type_router

router = APIRouter()
router.include_router(account_router, prefix="/account", tags=["Telegram Account"])
router.include_router(message_router, prefix="/messages", tags=["Telegram Messages"])
router.include_router(group_type_router, prefix="/group_type", tags=["Telegram Group Type"])
