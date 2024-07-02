from __future__ import annotations
from typing import TYPE_CHECKING, Any

from ..model import PlayerActivityHistory
from ._repository import Repository

if TYPE_CHECKING:
    from ... import BaseAsyncDatabase


class PlayerActivityHistoryRepository(Repository[PlayerActivityHistory, Any]):

    def __init__(self, database: BaseAsyncDatabase[Any]) -> None:
        super().__init__(database, PlayerActivityHistory)
