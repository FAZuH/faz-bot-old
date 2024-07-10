from datetime import datetime as dt

from sqlalchemy import Index, UniqueConstraint
from sqlalchemy.dialects.mysql import (
    BINARY,
    DATETIME,
    DECIMAL,
    INTEGER,
    SMALLINT,
    TINYINT,
    VARCHAR,
)
from sqlalchemy.orm import Mapped, mapped_column

from ._unique_id_model import UniqueIdModel


class GuildHistory(UniqueIdModel):
    __tablename__ = "guild_history"

    name: Mapped[str] = mapped_column(VARCHAR(30), nullable=False, primary_key=True)
    level: Mapped[float] = mapped_column(DECIMAL(5, 2, unsigned=True), nullable=False)
    territories: Mapped[int] = mapped_column(SMALLINT(unsigned=True), nullable=False)
    wars: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False)
    member_total: Mapped[int] = mapped_column(TINYINT(unsigned=True), nullable=False)
    online_members: Mapped[int] = mapped_column(TINYINT(unsigned=True), nullable=False)
    datetime: Mapped[dt] = mapped_column(DATETIME, nullable=False, primary_key=True)
    unique_id: Mapped[bytes] = mapped_column(BINARY(16), nullable=False)

    __table_args__ = (
        Index('datetime_idx', datetime.desc()),
        UniqueConstraint(unique_id, name='unique_id_idx')
    )
