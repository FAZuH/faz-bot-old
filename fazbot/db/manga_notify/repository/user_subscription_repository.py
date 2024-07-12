from __future__ import annotations
from typing import TYPE_CHECKING

from ..._base_repository import BaseRepository
from ..model import UserSubscription

if TYPE_CHECKING:
    from ..._base_async_database import BaseAsyncDatabase


class UserSubscriptionRepository(BaseRepository[UserSubscription, int]):

    def __init__(self, database: BaseAsyncDatabase) -> None:
        super().__init__(database, UserSubscription)
