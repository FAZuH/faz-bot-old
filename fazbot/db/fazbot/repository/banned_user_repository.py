from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import exists, select

from ..model import BannedUser
from ._repository import Repository

if TYPE_CHECKING:
    from ... import BaseAsyncDatabase


class BannedUserRepository(Repository[BannedUser, int]):

    def __init__(self, database: BaseAsyncDatabase) -> None:
        super().__init__(database, BannedUser)

    async def is_banned(self, user_i: int) -> bool:
        async with self.database.enter_session() as session:
            stmt = select(exists().where(self.get_model_cls().user_id == user_i))
            result = await session.execute(stmt)
            is_exist = result.scalar()
            return is_exist or False
