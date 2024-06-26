"""
Top level router for v1 API
"""
from fastapi import APIRouter

from app.config import settings
from .currency import router as currency_router
from .demo import router as demo_router
from .exchange_rate import router as exchange_rate_router
from .files import router as file_router
from .handling_fee import router as handling_fee_router
from .telegram import router as telegram_router
from .order import router as order_router
from .user import router as user_router

router = APIRouter()
router.include_router(telegram_router, prefix="/telegram", tags=["Telegram"])
router.include_router(currency_router, prefix="/currency", tags=["Currency"])
router.include_router(exchange_rate_router, prefix="/exchange_rate", tags=["Exchange Rate"])
router.include_router(file_router, prefix="/files", tags=["Files"])
router.include_router(handling_fee_router, prefix="/handling_fee", tags=["Handling Fee"])
router.include_router(order_router, prefix="/order", tags=["Order"])
router.include_router(user_router, prefix="/user", tags=["User"])

if settings.IS_DEV:
    router.include_router(demo_router, prefix="/demo", tags=["Demo"])
