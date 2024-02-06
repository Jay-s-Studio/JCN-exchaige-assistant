"""
Files Router
"""
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from app.handlers import FileHandler
from app.containers import Container

router = APIRouter()


@router.get(
    path="/{file_id}"
)
@inject
async def get_file(
    file_id: str,
    file_handler: FileHandler = Depends(Provide[Container.file_handler])
):
    """

    :param file_id:
    :param file_handler:
    :return:
    """
    return await file_handler.get_file(file_unique_id=file_id)
