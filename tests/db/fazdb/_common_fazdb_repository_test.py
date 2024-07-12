from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING

from fazbot.db.fazdb import FazdbDatabase

from .._common_db_repository_test import CommonDbRepositoryTest

if TYPE_CHECKING:
    from fazbot.db._base_repository import BaseRepository


class CommonFazdbRepositoryTest:

    class Test[R: BaseRepository](CommonDbRepositoryTest.Test[FazdbDatabase, R], ABC):

        # override
        @property
        def database_type(self) -> type[FazdbDatabase]:
            return FazdbDatabase

        @property
        def db_name(self) -> str:
            """Database name to be tested."""
            return "faz-db_test"
