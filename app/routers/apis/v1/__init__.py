"""
Top level router for v1 API
"""
from fastapi import APIRouter

from app.config import settings
from .currency import router as currency_router
from .demo import router as demo_router
from .exchange_rate import router as exchange_rate_router
from .handing_fee import router as handing_fee_router
from .telegram import router as telegram_router
from .user import router as user_router

router = APIRouter()
router.include_router(currency_router, prefix="/currency", tags=["Currency"])
router.include_router(exchange_rate_router, prefix="/exchange_rate", tags=["Exchange Rate"])
router.include_router(handing_fee_router, prefix="/handing_fee", tags=["Handing Fee"])
router.include_router(telegram_router, prefix="/telegram", tags=["Telegram"])
router.include_router(user_router, prefix="/user", tags=["User"])

if settings.IS_DEV:
    router.include_router(demo_router, prefix="/demo", tags=["Demo"])
