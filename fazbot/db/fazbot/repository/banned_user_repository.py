from typing import TYPE_CHECKING

from ..model import BannedUser
from . import Repository

if TYPE_CHECKING:
    from ... import BaseAsyncDatabase


class BannedUserRepository(Repository[BannedUser]):

    def __init__(self, database: BaseAsyncDatabase) -> None:
        self._model = BannedUser
        super().__init__(database, self._model)
