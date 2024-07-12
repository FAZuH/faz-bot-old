from __future__ import annotations
from typing import TYPE_CHECKING

from ..._base_repository import BaseRepository
from ..model import Manga

if TYPE_CHECKING:
    from ..._base_mysql_database import BaseMySQLDatabase


class MangaRepository(BaseRepository[Manga, tuple[str, str]]):

    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, Manga)
