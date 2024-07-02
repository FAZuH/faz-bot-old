from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from . import BaseModel


class BannedUser(BaseModel):
    __tablename__ = "banned_user"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    reason: Mapped[str] = mapped_column(String(255))
    from_: Mapped[datetime] = mapped_column(name="from")
    until: Mapped[Optional[datetime]] = mapped_column(default=None)

    def __repr__(self) -> str:
        return (
            "<BannedUser("
            f"user_id={self.user_id},"
            f"reason='{self.reason}',"
            f"from_={self.from_},"
            f"until={self.until}"
            ")>"
        )
