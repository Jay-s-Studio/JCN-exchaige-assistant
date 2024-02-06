"""
FileProvider
"""
import json

from redis.asyncio import Redis
from telegram import File, Bot

from app.config import settings
from app.libs.consts.enums import ExpireTime
from app.libs.database import RedisPool
from app.schemas.files import TelegramFile


class FileProvider:
    """FileProvider"""

    def __init__(
        self,
        bot: Bot,
        redis: RedisPool
    ):
        self._bot = bot
        self._redis: Redis = redis.create()

    @staticmethod
    def redis_name(name: str):
        """

        :return:
        """
        return f"{settings.APP_NAME}:{name}"

    async def set_file(self, file: TelegramFile):
        """

        :param file:
        :return:
        """
        redis_name = self.redis_name(name=f"files:{file.file_unique_id}")
        await self._redis.set(redis_name, value=file.model_dump_json(), ex=ExpireTime.ONE_WEEK.value)

    async def get_file(self, file_unique_id: str) -> TelegramFile:
        """

        :param file_unique_id:
        :return:
        """
        redis_name = self.redis_name(name=f"files:{file_unique_id}")
        value = await self._redis.get(redis_name)
        try:
            file_json = json.loads(value)
            file = File.de_json(file_json['file'], bot=self._bot)
        except Exception as e:
            raise e
        return TelegramFile(
            file_unique_id=file_unique_id,
            file=file,
            file_name=file_json['file_name'],
            content_type=file_json['content_type'],
        )
