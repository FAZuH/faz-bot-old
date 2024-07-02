from . import IFazbotDatabase
from .. import BaseAsyncDatabase
from .model import BaseModel
from .repository import BannedUserRepository, WhitelistedGuildRepository


class FazbotDatabase(BaseAsyncDatabase[BaseModel], IFazbotDatabase):

    def __init__(self, driver: str, user: str, password: str, host: str, port: int, database: str) -> None:
        super().__init__(driver, user, password, host, port, database)
        self._base_model = BaseModel()

        self._banned_user_repository = BannedUserRepository(self)
        self._whitelisted_guild_repository = WhitelistedGuildRepository(self)
        
    @property
    def banned_user_repository(self) -> BannedUserRepository:
        return self._banned_user_repository

    @property
    def whitelisted_guild_repository(self) -> WhitelistedGuildRepository:
        return self._whitelisted_guild_repository 

    # override
    @property
    def base_model(self) -> BaseModel:
        return self._base_model
