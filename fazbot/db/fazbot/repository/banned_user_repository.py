from typing import TYPE_CHECKING

from sqlalchemy import delete, exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..model import BannedUser
from . import Repository

if TYPE_CHECKING:
    from ... import BaseAsyncDatabase


class BannedUserRepository(Repository[BannedUser]):

    def __init__(self, database: BaseAsyncDatabase) -> None:
        super().__init__(database, BannedUser)

    async def delete(self, user_id: int, session: AsyncSession | None = None) -> None:
        async with self.database.must_enter_session(session) as session:
            model = self.get_model_cls()
            stmt = (
                delete(model).
                where(model.user_id == user_id)
            )
            await session.execute(stmt)

    async def is_banned(self, user_i: int) -> bool:
        async with self.database.enter_session() as session:
            stmt = select(exists().where(self.get_model_cls().user_id == user_i))
            result = await session.execute(stmt)
            is_exist = result.scalar()
            return is_exist or False
