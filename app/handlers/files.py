"""
FilesHandler
"""
import io

from fastapi.responses import StreamingResponse

from app.providers import FileProvider


class FileHandler:
    """FilesHandler"""

    def __init__(self, file_provider: FileProvider):
        self._file_provider = file_provider

    async def get_file(self, file_unique_id: str):
        """
        get file
        :param file_unique_id:
        :return:
        """
        telegram_file = await self._file_provider.get_file(file_unique_id=file_unique_id)
        file_content = await telegram_file.file.download_as_bytearray()
        return StreamingResponse(
            content=io.BytesIO(file_content),
            media_type=telegram_file.content_type,
            headers={
                "Content-Disposition": f"attachment; filename={telegram_file.file_name}"
            }
        )

