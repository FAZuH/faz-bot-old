from datetime import datetime as dt

from sqlalchemy import Index, UniqueConstraint
from sqlalchemy.dialects.mysql import BINARY, DATETIME, DECIMAL, ENUM, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from . import BaseModel


class PlayerHistory(BaseModel):
    __tablename__ = "player_history"

    uuid: Mapped[bytes] = mapped_column(BINARY(16), nullable=False, primary_key=True)
    username: Mapped[str] = mapped_column(VARCHAR(16), nullable=False)
    support_rank: Mapped[str] = mapped_column(VARCHAR(45), default=None)
    playtime: Mapped[float] = mapped_column(DECIMAL(8, 2, unsigned=True), nullable=False)
    guild_name: Mapped[str] = mapped_column(VARCHAR(30), default=None)
    guild_rank: Mapped[str] = mapped_column(ENUM('OWNER', 'CHIEF', 'STRATEGIST', 'CAPTAIN', 'RECRUITER', 'RECRUIT'), default=None)
    rank: Mapped[str] = mapped_column(VARCHAR(30), default=None)
    datetime: Mapped[dt] = mapped_column(DATETIME, nullable=False, primary_key=True)
    unique_id: Mapped[bytes] = mapped_column(BINARY(16), nullable=False)

    __table_args__ = (
        Index('datetime_idx', datetime.desc()),
        UniqueConstraint('unique_id', name='unique_id_idx')
    )
