from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING

from fazbot.db.manga_notify import MangaNotifyDatabase

from .._common_db_repository_test import CommonDbRepositoryTest

if TYPE_CHECKING:
    from fazbot.db._base_repository import BaseRepository


class CommonMangaNotifyRepositoryTest:

    class Test[R: BaseRepository](CommonDbRepositoryTest.Test[MangaNotifyDatabase, R], ABC):

        # override
        @property
        def database_type(self) -> type[MangaNotifyDatabase]:
            return MangaNotifyDatabase

        @property
        def db_name(self) -> str:
            """Database name to be tested."""
            return "manga_notify_test"
