from datetime import datetime
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from . import BaseModel


class BannedUser(BaseModel):
    __tablename__ = "banned_user"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    reason: Mapped[str] = mapped_column(String(255))
    from_: Mapped[datetime] = mapped_column(name="from")
    until: Mapped[Optional[datetime]] = mapped_column(default=None)
