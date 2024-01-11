"""Demo Router"""
from fastapi import APIRouter
from starlette.requests import Request

from app.libs.depends import DEFAULT_RATE_LIMITERS
from app.routing import LogRouting

router = APIRouter(
    dependencies=DEFAULT_RATE_LIMITERS,
    route_class=LogRouting
)


@router.get(
    path=""
)
async def get_demo(
    request: Request,
):
    """

    :param request:
    :return:
    """
    return {
        "message": "Hello World!"
    }
