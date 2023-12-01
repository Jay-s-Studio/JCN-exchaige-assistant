"""
Top level router for v1 API
"""
from fastapi import APIRouter

from .currency import router as currency_router
from .demo import router as demo_router
from .telegram import router as telegram_router

router = APIRouter()
router.include_router(currency_router, prefix="/currency", tags=["currency"])
router.include_router(demo_router, prefix="/demo", tags=["demo"])
router.include_router(telegram_router, prefix="/telegram", tags=["telegram"])
