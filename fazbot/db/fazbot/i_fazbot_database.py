from __future__ import annotations
from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from .repository import BannedUserRepository, WhitelistedGuildRepository


class IFazBotDatabase(Protocol):
    async def create_all_tables(self) -> None: ...
    @property
    def banned_user_repository(self) -> BannedUserRepository: ...
    @property
    def whitelisted_guild_repository(self) -> WhitelistedGuildRepository: ...

