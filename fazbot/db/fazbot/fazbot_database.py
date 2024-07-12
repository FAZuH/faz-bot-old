from .._base_async_database import BaseAsyncDatabase
from .model.base_fazbot_model import BaseFazbotModel
from .repository import *


class FazbotDatabase(BaseAsyncDatabase):

    def __init__(self, user: str, password: str, host: str, port: int, database: str) -> None:
        super().__init__(user, password, host, port, database)
        self._base_model = BaseFazbotModel()

        self._banned_user_repository = BannedUserRepository(self)
        self._whitelisted_guild_repository = WhitelistedGuildRepository(self)

        self.repositories.append(self.banned_user_repository)
        self.repositories.append(self.whitelisted_guild_repository)

    @property
    def banned_user_repository(self) -> BannedUserRepository:
        return self._banned_user_repository

    @property
    def whitelisted_guild_repository(self) -> WhitelistedGuildRepository:
        return self._whitelisted_guild_repository 

    @property
    def base_model(self) -> BaseFazbotModel:
        return self._base_model
