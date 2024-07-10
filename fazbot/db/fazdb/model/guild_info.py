from datetime import datetime as dt

from sqlalchemy.dialects.mysql import BINARY, DATETIME, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from .base_fazdb_model import BaseFazdbModel


class GuildInfo(BaseFazdbModel):
    __tablename__ = "guild_info"

    uuid: Mapped[bytes] = mapped_column(BINARY(16), primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    prefix: Mapped[str] = mapped_column(VARCHAR(4), nullable=False)
    created: Mapped[dt] = mapped_column(DATETIME, nullable=False)
