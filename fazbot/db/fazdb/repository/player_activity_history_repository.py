from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ..._base_repository import BaseRepository
from ..model import PlayerActivityHistory

if TYPE_CHECKING:
    from ..._base_mysql_database import BaseMySQLDatabase


class PlayerActivityHistoryRepository(BaseRepository[PlayerActivityHistory, Any]):

    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, PlayerActivityHistory)
