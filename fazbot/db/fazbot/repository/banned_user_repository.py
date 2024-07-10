from __future__ import annotations
from typing import TYPE_CHECKING, Any

from ..._base_repository import BaseRepository
from ..model import BannedUser

if TYPE_CHECKING:
    from ..._base_async_database import BaseAsyncDatabase


class BannedUserRepository(BaseRepository[BannedUser, int]):

    def __init__(self, database: BaseAsyncDatabase[Any]) -> None:
        super().__init__(database, BannedUser)
