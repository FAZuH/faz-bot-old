from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ..._base_repository import BaseRepository
from ..model import GuildHistory

if TYPE_CHECKING:
    from ..._base_mysql_database import BaseMySQLDatabase


class GuildHistoryRepository(BaseRepository[GuildHistory, Any]):

    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, GuildHistory)
