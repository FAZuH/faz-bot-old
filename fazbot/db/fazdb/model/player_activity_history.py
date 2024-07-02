from datetime import datetime as dt

from sqlalchemy import Index
from sqlalchemy.dialects.mysql import BINARY, DATETIME
from sqlalchemy.orm import Mapped, mapped_column

from . import BaseModel


class PlayerActivityHistory(BaseModel):
    __tablename__ = "player_activity_history"

    uuid: Mapped[bytes] = mapped_column(BINARY(16), nullable=False, primary_key=True)
    logon_datetime: Mapped[dt] = mapped_column(DATETIME, nullable=False, primary_key=True)
    logoff_datetime: Mapped[dt] = mapped_column(DATETIME, nullable=False)

    __table_args__ = (
        Index('logon_datetime_idx', logon_datetime.desc()),
        Index('logoff_datetime_idx', logoff_datetime.desc())
    )
