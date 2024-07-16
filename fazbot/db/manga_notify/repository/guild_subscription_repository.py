from __future__ import annotations
from typing import TYPE_CHECKING

from ..._base_repository import BaseRepository
from ..model import GuildSubscription

if TYPE_CHECKING:
    from ..._base_mysql_database import BaseMySQLDatabase


class GuildSubscriptionRepository(BaseRepository[GuildSubscription, int]):

    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, GuildSubscription)
