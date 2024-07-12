from datetime import datetime
from typing import Optional

from sqlalchemy.dialects.mysql import BIGINT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from .base_fazbot_model import BaseFazbotModel


class WhitelistedGuild(BaseFazbotModel):
    __tablename__ = "whitelisted_guild"

    guild_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    guild_name: Mapped[str] = mapped_column(VARCHAR(32))
    from_: Mapped[datetime] = mapped_column(name="from")
    until: Mapped[Optional[datetime]] = mapped_column(default=None)
