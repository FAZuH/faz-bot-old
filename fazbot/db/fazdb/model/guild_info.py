from datetime import datetime as dt

from sqlalchemy.dialects.mysql import BINARY, DATETIME, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from . import BaseModel


class GuildInfo(BaseModel):
    __tablename__ = "guild_info"

    name: Mapped[str] = mapped_column(VARCHAR(30), primary_key=True, nullable=False)
    prefix: Mapped[str] = mapped_column(VARCHAR(4), nullable=False)
    created: Mapped[dt] = mapped_column(DATETIME, nullable=False)
    uuid: Mapped[bytes] = mapped_column(BINARY(16), nullable=False)
