from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from . import BaseModel


class WhitelistedGuild(BaseModel):
    __tablename__ = "whitelisted_guild"

    guild_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    guild_name: Mapped[str] = mapped_column(String(32))
    from_: Mapped[datetime] = mapped_column(name="from")
    until: Mapped[Optional[datetime]] = mapped_column(default=None)

    def __repr__(self) -> str:
        return (
            "<WhitelistedGuild("
            f"guild_id={self.guild_id},"
            f"guild_name='{self.guild_name}',"
            f"from_={self.from_},"
            f"until={self.until}"
            ")>"
        )
