from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Sequence, TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..._base_repository import BaseRepository
from ..model import WhitelistGroup

if TYPE_CHECKING:
    from ..._base_mysql_database import BaseMySQLDatabase


class WhitelistGroupRepository(BaseRepository[WhitelistGroup, tuple[int, str]]):

    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, WhitelistGroup)

    async def ban_user(
        self,
        user_id: int,
        reason: str | None = None,
        until: datetime | None = None,
        *,
        session: AsyncSession | None = None
    ) -> None:
        async with self.database.must_enter_async_session(session) as ses:
            entity = self.model(id=user_id, type=self.Groups.BAN.value, reason=reason, until=until)
            await self.insert(entity, replace_on_duplicate=True, session=ses)

    async def unban_user(self, user_id: int, *, session: AsyncSession | None = None) -> None:
        async with self.database.must_enter_async_session(session) as ses:
            await self.delete((user_id, self.Groups.BAN.value), session=ses)

    async def is_banned_user(self, id: int, *, session: AsyncSession | None = None) -> bool:
        async with self.database.must_enter_async_session(session) as ses:
            return await self.is_exists((id, self.Groups.BAN.value), session=ses)

    async def whitelist_guild(
        self,
        guild_id: int,
        reason: str | None = None,
        until: datetime | None = None,
        *,
        session: AsyncSession | None = None
    ) -> None:
        async with self.database.must_enter_async_session(session) as ses:
            entity = self.model(id=guild_id, type=self.Groups.GUILD.value, reason=reason, until=until)
            await self.insert(entity, replace_on_duplicate=True, session=ses)

    async def unwhitelist_guild(self, guild_id: int, *, session: AsyncSession | None = None) -> None:
        async with self.database.must_enter_async_session(session) as ses:
            await self.delete((guild_id, self.Groups.GUILD.value), session=ses)

    async def is_whitelisted_guild(self, id: int, *, session: AsyncSession | None = None) -> bool:
        async with self.database.must_enter_async_session(session) as ses:
            return await self.is_exists((id, self.Groups.GUILD.value), session=ses)

    async def get_all_whitelisted_guild_ids(self, session: None | AsyncSession = None) -> Sequence[int]:
        async with self.database.must_enter_async_session(session) as session:
            stmt = select(self.model.id).where(self.model.type == self.Groups.GUILD.value)
            result = await session.execute(stmt)
            return result.scalars().all()


    class Groups(Enum):
        BAN = "ban"
        GUILD = "guild"
