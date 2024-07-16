from abc import ABC
from ._base_database import BaseDatabase


class BaseMySQLDatabase(BaseDatabase, ABC):

    def __init__(
            self,
            user: str,
            password: str,
            host: str,
            port: int,
            database: str,
        ) -> None:
        super().__init__("mysql+pymysql", "mysql+aiomysql", user, password, host, port, database)
