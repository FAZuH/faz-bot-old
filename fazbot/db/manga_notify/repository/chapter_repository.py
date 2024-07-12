from __future__ import annotations
from typing import TYPE_CHECKING

from ..._base_repository import BaseRepository
from ..model import Chapter

if TYPE_CHECKING:
    from ..._base_async_database import BaseAsyncDatabase


class ChapterRepository(BaseRepository[Chapter, bytes]):

    def __init__(self, database: BaseAsyncDatabase) -> None:
        super().__init__(database, Chapter)
