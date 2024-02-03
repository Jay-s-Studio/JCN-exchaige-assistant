"""
AccountProvider
"""
from typing import List, Tuple, Optional

import sqlalchemy as sa
from redis.asyncio import Redis

from app.libs.consts.enums import BotType
from app.libs.database import RedisPool, Session
from app.libs.decorators.sentry_tracer import distributed_trace
from app.models import SysTelegramAccount, SysTelegramChatGroup, SysTelegramChatGroupMember, SysCurrency
from app.models.handling_fee import SysHandlingFeeConfig
from app.serializers.v1.telegram import TelegramAccount, TelegramChatGroup, GroupMember, GroupInfo, UpdateGroupInfo


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
    async def set_group(self, chat_group: TelegramChatGroup):
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
                .on_conflict_do_nothing(constraint="unique_telegram_chat_group_member_key")
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
        try:
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
        except Exception as e:
            raise e
        else:
            return result
        finally:
            await self._session.close()

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
        try:
            customer_service = (
                self._session.select(
                    SysTelegramChatGroupMember.chat_group_id,
                    SysTelegramAccount.id,
                    SysTelegramAccount.username,
                    SysTelegramAccount.first_name,
                    SysTelegramAccount.last_name,
                    SysTelegramAccount.full_name,
                    SysTelegramAccount.name,
                    SysTelegramChatGroupMember.is_customer_service
                )
                .outerjoin(SysTelegramChatGroupMember, SysTelegramChatGroupMember.account_id == SysTelegramAccount.id)
                .where(SysTelegramChatGroupMember.is_customer_service.is_(True))
                .subquery()
            )
            result, count = await (
                self._session.select(
                    SysTelegramChatGroup.id,
                    SysTelegramChatGroup.title,
                    SysTelegramChatGroup.in_group,
                    SysTelegramChatGroup.bot_type,
                    SysTelegramChatGroup.description,
                    sa.func.array_agg(
                        sa.func.json_build_object(
                            sa.cast("id", sa.VARCHAR(32)), customer_service.c.id,
                            sa.cast("username", sa.VARCHAR(32)), customer_service.c.username,
                            sa.cast("first_name", sa.VARCHAR(32)), customer_service.c.first_name,
                            sa.cast("last_name", sa.VARCHAR(32)), customer_service.c.last_name,
                            sa.cast("full_name", sa.VARCHAR(32)), customer_service.c.full_name,
                            sa.cast("name", sa.VARCHAR(32)), customer_service.c.name,
                            sa.cast("is_customer_service", sa.VARCHAR(32)), customer_service.c.is_customer_service
                        )
                    ).label("customer_services"),
                    SysCurrency.symbol.label("currency_symbol"),
                    SysHandlingFeeConfig.name.label("handling_fee_name")
                )
                .outerjoin(customer_service, customer_service.c.chat_group_id == SysTelegramChatGroup.id)
                .outerjoin(SysCurrency, SysCurrency.id == SysTelegramChatGroup.currency_id)
                .outerjoin(SysHandlingFeeConfig, SysHandlingFeeConfig.id == SysTelegramChatGroup.handling_fee_config_id)
                .where(SysTelegramChatGroup.is_deleted.is_(False))
                .group_by(
                    SysTelegramChatGroup.id,
                    SysCurrency.symbol,
                    SysHandlingFeeConfig.name
                )
                .limit(page_size)
                .offset(page_index * page_size)
                .fetchpages(as_model=GroupInfo)
            )
        except Exception as e:
            raise e
        else:
            return result, count
        finally:
            await self._session.close()

    @distributed_trace()
    async def get_chat_group(self, group_id: int) -> Optional[GroupInfo]:
        """
        get a chat group
        :param group_id:
        :return:
        """
        try:
            customer_service = (
                self._session.select(
                    SysTelegramChatGroupMember.chat_group_id,
                    SysTelegramAccount.id,
                    SysTelegramAccount.username,
                    SysTelegramAccount.first_name,
                    SysTelegramAccount.last_name,
                    SysTelegramAccount.full_name,
                    SysTelegramAccount.name,
                    SysTelegramChatGroupMember.is_customer_service
                )
                .outerjoin(SysTelegramChatGroupMember, SysTelegramChatGroupMember.account_id == SysTelegramAccount.id)
                .where(SysTelegramChatGroupMember.is_customer_service.is_(True))
                .subquery()
            )
            result: Optional[GroupInfo] = await (
                self._session.select(
                    SysTelegramChatGroup.id,
                    SysTelegramChatGroup.title,
                    SysTelegramChatGroup.in_group,
                    SysTelegramChatGroup.bot_type,
                    SysTelegramChatGroup.description,
                    sa.func.array_agg(
                        sa.func.json_build_object(
                            sa.cast("id", sa.VARCHAR(32)), customer_service.c.id,
                            sa.cast("username", sa.VARCHAR(32)), customer_service.c.username,
                            sa.cast("first_name", sa.VARCHAR(32)), customer_service.c.first_name,
                            sa.cast("last_name", sa.VARCHAR(32)), customer_service.c.last_name,
                            sa.cast("full_name", sa.VARCHAR(32)), customer_service.c.full_name,
                            sa.cast("name", sa.VARCHAR(32)), customer_service.c.name,
                            sa.cast("is_customer_service", sa.VARCHAR(32)), customer_service.c.is_customer_service
                        )
                    ).label("customer_services"),
                    SysCurrency.symbol.label("currency_symbol"),
                    SysHandlingFeeConfig.name.label("handling_fee_name")
                )
                .outerjoin(customer_service, customer_service.c.chat_group_id == SysTelegramChatGroup.id)
                .outerjoin(SysCurrency, SysCurrency.id == SysTelegramChatGroup.currency_id)
                .outerjoin(SysHandlingFeeConfig, SysHandlingFeeConfig.id == SysTelegramChatGroup.handling_fee_config_id)
                .where(SysTelegramChatGroup.is_deleted.is_(False))
                .where(SysTelegramChatGroup.id == group_id)
                .group_by(
                    SysTelegramChatGroup.id,
                    SysCurrency.symbol,
                    SysHandlingFeeConfig.name
                )
                .fetchrow(as_model=GroupInfo)
            )
        except Exception as e:
            raise e
        else:
            return result
        finally:
            await self._session.close()

    @distributed_trace()
    async def update_group(self, group_id: int, group_info: UpdateGroupInfo):
        """
        update group
        :param group_id:
        :param group_info:
        :return:
        """
        data = group_info.model_dump(exclude={"customer_service_ids"})
        try:
            await (
                self._session.update(SysTelegramChatGroup)
                .where(SysTelegramChatGroup.id == group_id)
                .values(**data)
                .execute()
            )
        except Exception as e:
            await self._session.rollback()
            raise e
        else:
            await self._session.commit()
        finally:
            await self._session.close()

    @distributed_trace()
    async def update_customer_service(
        self,
        chat_group_id: int,
        account_id: int,
        is_customer_service: bool
    ):
        """
        update customer service
        :param chat_group_id:
        :param account_id:
        :param is_customer_service:
        :return:
        """
        try:
            await (
                self._session.update(SysTelegramChatGroupMember)
                .where(SysTelegramChatGroupMember.chat_group_id == chat_group_id)
                .where(SysTelegramChatGroupMember.account_id == account_id)
                .values(is_customer_service=is_customer_service)
                .execute()
            )
        except Exception as e:
            await self._session.rollback()
            raise e
        else:
            await self._session.commit()
        finally:
            await self._session.close()

    @distributed_trace()
    async def get_chat_group_members(
        self,
        chat_group_id: int
    ) -> List[GroupMember]:
        """
        get chat group members
        :param chat_group_id:
        :return:
        """
        try:
            members = await (
                self._session.select(
                    SysTelegramAccount.id,
                    SysTelegramAccount.username,
                    SysTelegramAccount.first_name,
                    SysTelegramAccount.last_name,
                    SysTelegramAccount.full_name,
                    SysTelegramAccount.name,
                    SysTelegramChatGroupMember.is_customer_service
                )
                .outerjoin(
                    SysTelegramChatGroupMember,
                    SysTelegramChatGroupMember.account_id == SysTelegramAccount.id
                )
                .where(SysTelegramChatGroupMember.chat_group_id == chat_group_id)
                .where(SysTelegramChatGroupMember.is_deleted.is_(False))
                .fetch(as_model=GroupMember)
            )
        except Exception as e:
            raise e
        else:
            return members
        finally:
            await self._session.close()
