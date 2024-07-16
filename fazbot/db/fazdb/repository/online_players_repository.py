from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ..._base_repository import BaseRepository
from ..model import OnlinePlayers

if TYPE_CHECKING:
    from ..._base_mysql_database import BaseMySQLDatabase


class OnlinePlayersRepository(BaseRepository[OnlinePlayers, Any]):

    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, OnlinePlayers)
