from datetime import datetime
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from . import BaseModel


class WhitelistedGuild(BaseModel):
    __tablename__ = "whitelisted_guild"

    guild_id: Mapped[int] = mapped_column(primary_key=True)
    guild_name: Mapped[str] = mapped_column(String(32))
    from_: Mapped[datetime] = mapped_column(name="from")
    until: Mapped[Optional[datetime]] = mapped_column(default=None)
