from datetime import datetime as dt

from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import Mapped, mapped_column

from . import BaseModel


class FazdbUptime(BaseModel):
    __tablename__ = "fazdb_uptime"

    start_time: Mapped[dt] = mapped_column(DATETIME, primary_key=True, nullable=False)
    stop_time: Mapped[dt] = mapped_column(DATETIME, nullable=False)
