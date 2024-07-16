from __future__ import annotations
from typing import Sequence, TYPE_CHECKING

from sqlalchemy import select

from ..._base_repository import BaseRepository
from ..model import WhitelistedGuild

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from ..._base_mysql_database import BaseMySQLDatabase


class WhitelistedGuildRepository(BaseRepository[WhitelistedGuild, int]):

    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, WhitelistedGuild)

    async def get_all_whitelisted_guild_ids(self, session: None | AsyncSession = None) -> Sequence[int]:
        async with self.database.must_enter_async_session(session) as session:
            stmt = select(self.model.guild_id)
            result = await session.execute(stmt)
            whitelisted_guilds = result.scalars().all()
        return whitelisted_guilds
