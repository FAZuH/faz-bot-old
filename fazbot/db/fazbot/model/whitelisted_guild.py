from __future__ import annotations
from typing import TYPE_CHECKING, Any

from . import Model

if TYPE_CHECKING:
    from datetime import datetime


class WhitelistedGuild(Model):

    def __init__(self, guild_id: int, guild_name: str, from_: datetime, until: datetime | None) -> None:
        self._guild_id = guild_id
        self._guild_name = guild_name
        self._from = from_
        self._until = until

    # override
    def to_dict(self) -> dict[str, Any]:
        return {
            "guild_id": self._guild_id,
            "guild_name": self._guild_name,
            "from": self._from,
            "until": self._until,
        }

    # override
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WhitelistedGuild:
        return cls(data["guild_id"], data["guild_name"], data["from"], data["until"])

    @property
    def guild_id(self) -> int:
        return self._guild_id

    @property
    def guild_name(self) -> str:
        return self._guild_name

    @property
    def from_(self) -> datetime:
        return self._from

    @property
    def until(self) -> datetime | None:
        return self._until
