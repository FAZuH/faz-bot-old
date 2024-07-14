from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ..._base_repository import BaseRepository
from ..model import PlayerInfo

if TYPE_CHECKING:
    from ..._base_mysql_database import BaseMySQLDatabase


class PlayerInfoRepository(BaseRepository[PlayerInfo, Any]):

    def __init__(self, database: BaseMySQLDatabase[Any]) -> None:
        super().__init__(database, PlayerInfo)