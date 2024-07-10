from datetime import datetime as dt

from sqlalchemy.dialects.mysql import BINARY, DATETIME, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from .base_fazdb_model import BaseFazdbModel


class PlayerInfo(BaseFazdbModel):
    __tablename__ = "player_info"

    uuid: Mapped[bytes] = mapped_column(BINARY(16), primary_key=True, nullable=False)
    latest_username: Mapped[str] = mapped_column(VARCHAR(16), nullable=False)
    first_join: Mapped[dt] = mapped_column(DATETIME, nullable=False)
