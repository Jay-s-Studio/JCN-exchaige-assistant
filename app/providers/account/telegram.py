"""
AccountProvider
"""
from datetime import datetime
from typing import Optional, List, Tuple

from redis.asyncio import Redis

from app.clients.firebase.firestore import GoogleFirestoreClient
from app.libs.consts.enums import BotType
from app.libs.database import RedisPool, Session
from app.libs.decorators.sentry_tracer import distributed_trace
from app.libs.logger import logger
from app.models import SysTelegramAccount, SysTelegramChatGroup, SysTelegramAccountGroupRelation
from app.schemas.account.telegram import TelegramAccount, TelegramChatGroup


class TelegramAccountProvider:
    """TelegramAccountProvider"""

    def __init__(
        self,
        session: Session,
        redis: RedisPool
    ):
        self._session = session
        self._redis: Redis = redis.create()
        self.firestore_client = GoogleFirestoreClient()

    @staticmethod
    def redis_name():
        """

        :return:
        """

    @distributed_trace()
    async def set_account(self, account: TelegramAccount):
        """
        set account
        :param account:
        :return:
        """
        data = account.model_dump(exclude={"updated_at"}, exclude_none=True)
        update_data = account.model_dump(exclude={"id", "created_at", "created_by", "updated_by"}, exclude_none=True)
        try:
            await (
                self._session.insert(SysTelegramAccount)
                .values(**data)
                .on_conflict_do_update(index_elements=["id"], set_=update_data)
                .execute()
            )
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise e
        finally:
            await self._session.close()

    @distributed_trace()
    async def get_account(self, user_id: str) -> Optional[TelegramAccount]:
        """
        get account
        :param user_id:
        :return:
        """
        result = await self.firestore_client.get_document(
            collection="account",
            document=user_id
        )
        if not result.exists:
            return None
        return TelegramAccount(**result.to_dict())

    @distributed_trace()
    async def update_chat_group(self, chat_group: TelegramChatGroup):
        """
        update a chat group
        :param chat_group:
        :return:
        """
        data = chat_group.model_dump(exclude={"updated_at"}, exclude_none=True)
        update_data = chat_group.model_dump(exclude={"id", "created_at", "created_by", "updated_by"}, exclude_none=True)
        try:
            await (
                self._session.insert(SysTelegramChatGroup)
                .values(**data)
                .on_conflict_do_update(index_elements=["id"], set_=update_data)
                .execute()
            )
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise e
        finally:
            await self._session.close()

    @distributed_trace()
    async def get_chat_group(self, chat_id: int) -> Optional[TelegramChatGroup]:
        """
        get a chat group
        :param chat_id:
        :return:
        """
        result = await (
            self._session.select(SysTelegramChatGroup)
            .where(SysTelegramChatGroup.id == chat_id)
            .fetchrow(as_model=TelegramChatGroup)
        )
        if not result:
            return None
        return result

    @distributed_trace()
    async def get_all_chat_group(self) -> List[TelegramChatGroup]:
        """
        get all chat group
        :return:
        """
        chat_groups = []
        async for item in self.firestore_client.stream(collection="chat_group"):
            chat_groups.append(TelegramChatGroup(**item.to_dict()))
        return chat_groups

    @distributed_trace()
    async def get_chat_groups_by_bot_type(self, bot_type: BotType) -> List[TelegramChatGroup]:
        """
        get chat groups by bot type
        :param bot_type:
        :return:
        """
        result: List[TelegramChatGroup] = await self.get_all_chat_group()
        chat_groups = []
        for item in result:
            if item.custom_info.bot_type == bot_type:
                chat_groups.append(item)
        return chat_groups

    @distributed_trace()
    async def update_account_group_relation(self, account_id: int, chat_group_id: int):
        """
        update chat group member
        :param account_id:
        :param chat_group_id:
        :return:
        """
        data = {
            "account_id": account_id,
            "chat_group_id": chat_group_id
        }
        try:
            await (
                self._session.insert(SysTelegramAccountGroupRelation)
                .values(**data)
                .on_conflict_do_nothing(constraint="unique_telegram_account_group_relation_uc")
                .execute()
            )
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise e
        finally:
            await self._session.close()

    @distributed_trace()
    async def get_chat_group_members(
        self,
        chat_id: int,
        page_size: int = 20,
        page_index: int = 0
    ) -> Tuple[List[TelegramAccount], int]:
        """
        get chat group members
        :param chat_id:
        :param page_size:
        :param page_index:
        :return:
        """
        accounts, count = await (
            self._session.select(SysTelegramAccount)
            .outerjoin(
                SysTelegramAccountGroupRelation,
                SysTelegramAccountGroupRelation.account_id == SysTelegramAccount.id
            )
            .where(SysTelegramAccountGroupRelation.chat_group_id == chat_id)
            .limit(page_size)
            .offset(page_index * page_size)
            .fetchpages(as_model=TelegramAccount)
        )
        return accounts, count

    @distributed_trace()
    async def delete_chat_group_member(self, chat_id: int, user_id: int):
        """
        delete chat group member
        :param chat_id:
        :param user_id:
        :return:
        """
        try:
            await (
                self._session.delete(SysTelegramAccountGroupRelation)
                .where(SysTelegramAccountGroupRelation.chat_group_id == chat_id)
                .where(SysTelegramAccountGroupRelation.account_id == user_id)
                .execute()
            )
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise e
        finally:
            await self._session.close()

    @distributed_trace()
    async def update_group_custom_info(
        self,
        chat_id: str,
        data: dict,
    ) -> bool:
        """
        update group customer service
        :param chat_id:
        :param data:
        :return:
        """
        _collection = "chat_group"
        result = await self.firestore_client.get_document(
            collection=_collection,
            document=chat_id
        )
        if not result.exists:
            return False
        await self.firestore_client.update_document(
            collection=_collection,
            document=chat_id,
            data=data
        )
        return True
