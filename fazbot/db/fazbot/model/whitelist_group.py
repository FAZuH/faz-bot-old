from datetime import datetime
from typing import Optional, Any

from sqlalchemy.dialects.mysql import BIGINT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from .base_fazbot_model import BaseFazbotModel


class WhitelistGroup(BaseFazbotModel):
    __tablename__ = "whitelist_group"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    type: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    reason: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    from_: Mapped[datetime] = mapped_column(name="from")
    until: Mapped[Optional[datetime]] = mapped_column(default=None)

    def __init__(
        self,
        *,
        id: int,
        type: str,
        reason: str | None = None,
        from_: datetime | None = None,
        until: datetime | None = None,
        **kw: Any
    ) -> None:
        self.id = id
        self.type = type
        self.reason = reason
        self.from_ = from_ or datetime.now()
        self.until = until
        super().__init__(**kw)
