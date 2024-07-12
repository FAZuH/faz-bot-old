from __future__ import annotations
from typing import TYPE_CHECKING

from ..._base_repository import BaseRepository
from ..model import UserSubscription

if TYPE_CHECKING:
    from ..._base_mysql_database import BaseMySQLDatabase


class UserSubscriptionRepository(BaseRepository[UserSubscription, int]):

    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, UserSubscription)
