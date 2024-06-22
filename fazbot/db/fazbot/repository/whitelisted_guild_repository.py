from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import select

from ..model import WhitelistedGuild
from ._repository import Repository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from ... import BaseAsyncDatabase


class WhitelistedGuildRepository(Repository[WhitelistedGuild, int]):

    def __init__(self, database: BaseAsyncDatabase[WhitelistedGuild]) -> None:
        super().__init__(database, WhitelistedGuild)

    async def get_all_whitelisted_guild_ids(self, session: None | AsyncSession = None) -> list[int]:
        model = self.get_model_cls()
        async with self.database.must_enter_session(session) as session:
            stmt = select(model)
            result = await session.execute(stmt)
            whitelisted_guilds = result.scalars().all()

        whitelisted_guild_ids = [guild.guild_id for guild in whitelisted_guilds]
        return whitelisted_guild_ids
