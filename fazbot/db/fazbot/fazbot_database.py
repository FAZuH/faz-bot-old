from .._base_mysql_database import BaseMySQLDatabase
from .model.base_fazbot_model import BaseFazbotModel
from .repository import *


class FazbotDatabase(BaseMySQLDatabase):

    def __init__(self, user: str, password: str, host: str, port: int, database: str) -> None:
        super().__init__(user, password, host, port, database)
        self._base_model = BaseFazbotModel()

        self._whitelist_group_repository = WhitelistGroupRepository(self)
        self.repositories.append(self.whitelist_group_repository)

    @property
    def whitelist_group_repository(self) -> WhitelistGroupRepository:
        return self._whitelist_group_repository

    @property
    def base_model(self) -> BaseFazbotModel:
        return self._base_model
