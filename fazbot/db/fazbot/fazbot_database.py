from .. import BaseAsyncDatabase
from .model import BaseModel


class FazBotDatabase(BaseAsyncDatabase[BaseModel]):

    def __init__(self, driver: str, user: str, password: str, host: str, database: str) -> None:
        super().__init__(driver, user, password, host, database)    
        self._base_model = BaseModel()

    # override
    @property
    def base_model(self) -> BaseModel:
        return self._base_model
