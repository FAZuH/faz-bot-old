from datetime import datetime

from sqlalchemy.dialects.mysql import DATETIME, SMALLINT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from .base_fazdb_model import BaseFazdbModel


class Worlds(BaseFazdbModel):
    __tablename__ = "worlds"

    name: Mapped[str] = mapped_column(VARCHAR(16), nullable=False, primary_key=True)
    player_count: Mapped[int] = mapped_column(SMALLINT(unsigned=True), nullable=False)
    time_created: Mapped[datetime] = mapped_column(DATETIME, nullable=False)
