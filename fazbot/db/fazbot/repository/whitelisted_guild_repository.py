from typing import TYPE_CHECKING

from ..model import WhitelistedGuild
from . import Repository

if TYPE_CHECKING:
    from ... import BaseAsyncDatabase


class WhitelistedGuildRepository(Repository[WhitelistedGuild]):

    def __init__(self, database: BaseAsyncDatabase) -> None:
        super().__init__(database, WhitelistedGuild)
