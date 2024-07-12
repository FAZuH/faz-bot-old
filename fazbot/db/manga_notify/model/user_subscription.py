from __future__ import annotations
from typing import Any, TYPE_CHECKING

from sqlalchemy.dialects.mysql import BIGINT, BOOLEAN
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._manga_user_subscription import manga_user_subscription
from .base_manga_notify_model import BaseMangaNotifyModel

if TYPE_CHECKING:
    from . import Manga


class UserSubscription(BaseMangaNotifyModel):
    __tablename__ = "user_subscription"

    user_id = mapped_column(BIGINT, primary_key=True)
    is_notify = mapped_column(BOOLEAN, nullable=False, default=False)

    subscribed_mangas: Mapped[list[Manga]] = relationship(
        "Manga",
        secondary=manga_user_subscription,
        back_populates="subscribed_users"
    )

    def __init__(self, *, user_id: int, is_notify: bool, **kw: Any):
        self.user_id = user_id
        self.is_notify = is_notify
        super().__init__(**kw)
