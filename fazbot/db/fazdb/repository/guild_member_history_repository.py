from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ..._base_repository import BaseRepository
from ..model import GuildMemberHistory

if TYPE_CHECKING:
    from ..._base_async_database import BaseAsyncDatabase


class GuildMemberHistoryRepository(BaseRepository[GuildMemberHistory, Any]):

    def __init__(self, database: BaseAsyncDatabase[Any]) -> None:
        super().__init__(database, GuildMemberHistory)
