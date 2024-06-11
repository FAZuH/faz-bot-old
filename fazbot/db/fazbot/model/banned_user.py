from __future__ import annotations
from typing import TYPE_CHECKING, Any

from . import Model

if TYPE_CHECKING:
    from datetime import datetime


class BannedUser(Model):

    def __init__(self, user_id: int, reason: str, from_: datetime, until: datetime | None):
        self._user_id = user_id
        self._reason = reason
        self._from = from_
        self._until = until

    # override
    def to_dict(self) -> dict[str, Any]:
        return {
            "user_id": self._user_id,
            "reason": self._reason,
            "from": self._from,
            "until": self._until,
        }

    # override
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BannedUser:
        return cls(
            data["user_id"],
            data["reason"],
            data["from"],
            data["until"],
        )

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def reason(self) -> str:
        return self._reason

    @property
    def from_(self) -> datetime:
        return self._from

    @property
    def until(self) -> datetime | None:
        return self._until
