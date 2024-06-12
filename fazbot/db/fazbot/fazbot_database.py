import asyncio
from typing import TYPE_CHECKING
from . import IFazBotDatabase
from .repository import BannedUserRepository, WhitelistedGuildRepository
from .. import DatabaseQuery

if TYPE_CHECKING:
    from .repository import Repository


class FazBotDatabase(IFazBotDatabase):

    def __init__(
            self,
            user: str,
            password: str,
            database: str,
            retries: int
        ) -> None:
        self._db = DatabaseQuery("localhost", user, password, database, retries)

        self._banned_user_repository = BannedUserRepository(self._db)
        self._whitelisted_guild_repository = WhitelistedGuildRepository(self._db)

        self._repositories: list[Repository] = [
            self._banned_user_repository,
            self._whitelisted_guild_repository
        ]

    async def create_all_tables(self):
        for repo in self._repositories:
            await repo.create_table()

    @property
    def banned_user_repository(self) -> BannedUserRepository:
        return self._banned_user_repository

    @property
    def whitelisted_guild_repository(self) -> WhitelistedGuildRepository:
        return self._whitelisted_guild_repository

