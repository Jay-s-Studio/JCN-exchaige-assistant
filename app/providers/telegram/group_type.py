"""
TelegramGroupTypeProvider
"""
from uuid import UUID

from app.libs.database import Session
from app.libs.decorators.sentry_tracer import distributed_trace

from app.models import SysTelegramChatGroupType, SysTelegramChatGroupTypeRelation
from app.schemas.group_type import GroupTypeRelation
from app.serializers.v1.telegram.group_type import TelegramGroupType


class TelegramGroupTypeProvider:
    """TelegramGroupTypeProvider"""

    def __init__(self, session: Session):
        self._session = session

    @distributed_trace()
    async def get_group_types(self):
        """
        get group types
        :return:
        """
        try:
            result = await (
                self._session.select(
                    SysTelegramChatGroupType.id,
                    SysTelegramChatGroupType.name
                )
                .order_by(SysTelegramChatGroupType.created_at.desc())
                .fetch(as_model=TelegramGroupType)
            )
        except Exception as e:
            raise e
        else:
            return result
        finally:
            await self._session.close()

    @distributed_trace()
    async def create_group_type(self, group_type: TelegramGroupType) -> UUID:
        """
        create a group type
        :return:
        """
        values = group_type.model_dump()
        try:
            await (
                self._session.insert(SysTelegramChatGroupType)
                .values(values)
                .execute()
            )
        except Exception as e:
            raise e
        else:
            await self._session.commit()
            return group_type.id
        finally:
            await self._session.close()

    @distributed_trace()
    async def update_group_type(self, group_type: TelegramGroupType) -> None:
        """
        update a group type
        :return:
        """
        values = group_type.model_dump(exclude={"id"})
        try:
            await (
                self._session.update(SysTelegramChatGroupType)
                .values(values)
                .where(SysTelegramChatGroupType.id == group_type.id)
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
    async def delete_group_type(self, group_type_id: UUID) -> None:
        """
        delete a group type
        :return:
        """
        try:
            await (
                self._session.delete(SysTelegramChatGroupType)
                .where(SysTelegramChatGroupType.id == group_type_id)
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
    async def create_group_type_relation(self, group_type_relation: GroupTypeRelation) -> None:
        """
        create a group type relation
        :return:
        """
        values = group_type_relation.model_dump()
        try:
            await (
                self._session.insert(SysTelegramChatGroupTypeRelation)
                .values(values)
                .execute()
            )
        except Exception as e:
            raise e
        else:
            await self._session.commit()
        finally:
            await self._session.close()
