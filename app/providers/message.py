"""
MessageProvider
"""
from uuid import UUID

from app.libs.consts.enums import BotType
from app.libs.database import Session

from app.models import SysMessage, SysMessageHistory
from app.schemas.broadcast_message import BroadcastMessage, BroadcastMessageHistory


class MessageProvider:
    """MessageProvider"""

    def __init__(self, session: Session):
        self._session = session

    async def create_message(self, message: BroadcastMessage) -> UUID:
        """
        create message
        :param message:
        :return:
        """
        value = message.model_dump(exclude_none=True)
        try:
            await (
                self._session.insert(SysMessage)
                .values(value)
                .execute()
            )
        except Exception as e:
            await self._session.rollback()
            raise e
        else:
            await self._session.commit()
            return message.id
        finally:
            await self._session.close()

    async def create_message_history(self, message_history: BroadcastMessageHistory):
        """
        create message history
        :param message_history:
        :return:
        """
        value = message_history.model_dump(exclude_none=True)
        try:
            await (
                self._session.insert(SysMessageHistory)
                .values(value)
                .execute()
            )
        except Exception as e:
            await self._session.rollback()
            raise e
        else:
            await self._session.commit()
        finally:
            await self._session.close()

    async def update_message_history(self, message_history: BroadcastMessageHistory):
        """
        update message history
        :param message_history:
        :return:
        """
        value = message_history.model_dump(exclude={"id", "message_id", "chat_group_id"}, exclude_none=True)
        try:
            await (
                self._session.update(SysMessageHistory)
                .where(SysMessageHistory.id == message_history.id)
                .values(value)
                .execute()
            )
        except Exception as e:
            await self._session.rollback()
            raise e
        else:
            await self._session.commit()
        finally:
            await self._session.close()
