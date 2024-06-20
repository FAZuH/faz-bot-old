from .. import BaseAsyncDatabase
from .model import BaseModel


class FazBotDatabase(BaseAsyncDatabase):

    def __init__(self, driver: str, user: str, password: str, host: str, database: str) -> None:
        super().__init__(driver, user, password, host, database)    
        self._base_model = BaseModel()

    @property
    def base_model(self) -> BaseModel:
        return self._base_model
