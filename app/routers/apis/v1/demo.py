"""Demo Router"""
from fastapi import APIRouter, UploadFile
from starlette.requests import Request

from app.libs.depends import DEFAULT_RATE_LIMITERS
from app.route_classes import LogRoute

router = APIRouter(
    dependencies=DEFAULT_RATE_LIMITERS,
    route_class=LogRoute
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


@router.post(
    path="/upload_file"
)
async def post_demo(
    file: UploadFile
):
    """

    :param file:
    :return:
    """
    return {
        "name": file.filename,
        "content_type": file.content_type
    }
