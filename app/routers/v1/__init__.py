"""
Top level router for v1 API
"""
from fastapi import APIRouter

from .currency import router as currency_router
from .demo import router as demo_router
from .telegram import router as telegram_router
from .exchange_rate import router as exchange_rate_router

router = APIRouter()
router.include_router(currency_router, prefix="/currency", tags=["currency"])
router.include_router(demo_router, prefix="/demo", tags=["demo"])
router.include_router(exchange_rate_router, prefix="/exchange_rate", tags=["exchange_rate"])
router.include_router(telegram_router, prefix="/telegram", tags=["telegram"])
