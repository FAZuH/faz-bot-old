from __future__ import annotations
from typing import TYPE_CHECKING, Any

from ..model import CharacterHistory
from ._repository import Repository

if TYPE_CHECKING:
    from ... import BaseAsyncDatabase


class CharacterHistoryRepository(Repository[CharacterHistory, Any]):

    def __init__(self, database: BaseAsyncDatabase[Any]) -> None:
        super().__init__(database, CharacterHistory)
