from __future__ import annotations
from typing import TYPE_CHECKING, Any
from dataclasses import dataclass

from . import Model

if TYPE_CHECKING:
    from datetime import datetime


@dataclass
class BannedUser(Model):
    user_id: int
    reason: str
    from_: datetime
    until: datetime | None

    # override
    def to_dict(self) -> dict[str, Any]:
        return {
            "user_id": self.user_id,
            "reason": self.reason,
            "from": self.from_,
            "until": self.until,
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

