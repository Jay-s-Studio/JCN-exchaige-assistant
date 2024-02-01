"""
AccountProvider
"""
from typing import List, Tuple

import sqlalchemy as sa
from redis.asyncio import Redis

from app.libs.consts.enums import BotType
from app.libs.database import RedisPool, Session
from app.libs.decorators.sentry_tracer import distributed_trace
from app.models import SysTelegramAccount, SysTelegramChatGroup, SysTelegramChatGroupMember, SysCurrency
from app.models.handing_fee import SysHandingFeeConfig
from app.serializers.v1.telegram import TelegramAccount, TelegramChatGroup, GroupMember, GroupInfo


class TelegramAccountProvider:
    """TelegramAccountProvider"""

    def __init__(
        self,
        session: Session,
        redis: RedisPool
    ):
        self._session = session
        self._redis: Redis = redis.create()

    @distributed_trace()
    async def set_account(self, account: TelegramAccount):
        """
        set account
        :param account:
        :return:
        """
        data = account.model_dump(exclude_none=True)
        update_data = account.model_dump(exclude={"id"}, exclude_none=True)
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
    async def update_chat_group(self, chat_group: TelegramChatGroup):
        """
        update a chat group
        :param chat_group:
        :return:
        """
        data = chat_group.model_dump(exclude_none=True)
        update_data = chat_group.model_dump(exclude={"id"}, exclude_none=True)
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
    async def init_chat_group_member(self, data: dict):
        """
        Initialize chat group member
        :param data:
        :return:
        """
        try:
            await (
                self._session.insert(SysTelegramChatGroupMember)
                .values(**data)
                .on_conflict_do_nothing(constraint="unique_telegram_chat_group_member_uc")
                .execute()
            )
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise e
        finally:
            await self._session.close()

    @distributed_trace()
    async def delete_chat_group_member(self, account_id: int, group_id: int, force: bool = False):
        """
        delete chat group member
        :param account_id:
        :param group_id:
        :param force:
        :return:
        """
        try:
            if force:
                await (
                    self._session.delete(SysTelegramChatGroupMember)
                    .where(SysTelegramChatGroupMember.account_id == account_id)
                    .where(SysTelegramChatGroupMember.chat_group_id == group_id)
                    .execute()
                )
            else:
                await (
                    self._session.update(SysTelegramChatGroupMember)
                    .where(SysTelegramChatGroupMember.account_id == account_id)
                    .where(SysTelegramChatGroupMember.chat_group_id == group_id)
                    .values(is_deleted=True)
                    .execute()
                )
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise e
        finally:
            await self._session.close()

    @distributed_trace()
    async def get_chat_group_by_bot_type(self, bot_type: BotType) -> List[TelegramChatGroup]:
        """
        get a chat group by bot type
        :param bot_type:
        :return:
        """
        result = await (
            self._session.select(
                SysTelegramChatGroup.id,
                SysTelegramChatGroup.title,
                SysTelegramChatGroup.type,
                SysTelegramChatGroup.in_group,
                SysTelegramChatGroup.bot_type
            )
            .where(SysTelegramChatGroup.bot_type == bot_type)
            .fetch(as_model=TelegramChatGroup)
        )
        return result

    @distributed_trace()
    async def get_chat_groups(
        self,
        page_size: int = 20,
        page_index: int = 0
    ) -> Tuple[List[GroupInfo], int]:
        """
        get the chat groups
        :return:
        """
        result, count = await (
            self._session.select(
                SysTelegramChatGroup.id,
                SysTelegramChatGroup.title,
                SysTelegramChatGroup.in_group,
                SysTelegramChatGroup.bot_type,
                SysTelegramChatGroup.description,
                sa.func.array_agg(SysTelegramChatGroupMember.account_id).label("customer_service_ids"),
                SysCurrency.symbol.label("currency_symbol"),
                SysHandingFeeConfig.name.label("handling_fee_name")
            )
            .outerjoin(SysTelegramChatGroupMember, SysTelegramChatGroupMember.chat_group_id == SysTelegramChatGroup.id)
            .outerjoin(SysCurrency, SysCurrency.id == SysTelegramChatGroup.currency_id)
            .outerjoin(SysHandingFeeConfig, SysHandingFeeConfig.id == SysTelegramChatGroup.handing_fee_config_id)
            .where(SysTelegramChatGroup.is_deleted.is_(False))
            .where(SysTelegramChatGroupMember.is_customer_service.is_(True))
            .group_by(
                SysTelegramChatGroup.id,
                SysCurrency.symbol,
                SysHandingFeeConfig.name
            )
            .limit(page_size)
            .offset(page_index * page_size)
            .fetchpages(as_model=GroupInfo)
        )
        return result, count

    @distributed_trace()
    async def get_chat_group_members(
        self,
        chat_id: int
    ) -> List[GroupMember]:
        """
        get chat group members
        :param chat_id:
        :return:
        """
        members = await (
            self._session.select(
                SysTelegramAccount.id,
                SysTelegramAccount.username,
                SysTelegramAccount.first_name,
                SysTelegramAccount.last_name,
                SysTelegramAccount.full_name,
                SysTelegramAccount.name
            )
            .outerjoin(
                SysTelegramChatGroupMember,
                SysTelegramChatGroupMember.account_id == SysTelegramAccount.id
            )
            .where(SysTelegramChatGroupMember.chat_group_id == chat_id)
            .where(SysTelegramChatGroupMember.is_deleted.is_(False))
            .fetch(as_model=GroupMember)
        )
        return members
