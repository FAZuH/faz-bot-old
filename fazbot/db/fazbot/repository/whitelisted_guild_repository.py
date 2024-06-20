from typing import TYPE_CHECKING

from sqlalchemy import delete, exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..model import WhitelistedGuild
from . import Repository

if TYPE_CHECKING:
    from ... import BaseAsyncDatabase


class WhitelistedGuildRepository(Repository[WhitelistedGuild]):

    def __init__(self, database: BaseAsyncDatabase) -> None:
        super().__init__(database, WhitelistedGuild)

    async def delete(self, guild_id: int, session: AsyncSession | None = None) -> None:
        async with self.database.must_enter_session(session) as session:
            model = self.get_model_cls()
            stmt = (
                delete(model).
                where(model.guild_id == guild_id)
            )
            await session.execute(stmt)
