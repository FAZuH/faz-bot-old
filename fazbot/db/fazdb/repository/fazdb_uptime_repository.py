from __future__ import annotations
from typing import TYPE_CHECKING, Any

from ..model import FazdbUptime
from ._repository import Repository

if TYPE_CHECKING:
    from ... import BaseAsyncDatabase


class FazdbUptimeRepository(Repository[FazdbUptime, Any]):

    def __init__(self, database: BaseAsyncDatabase[Any]) -> None:
        super().__init__(database, FazdbUptime)
