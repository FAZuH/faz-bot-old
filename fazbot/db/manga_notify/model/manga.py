from __future__ import annotations
from typing import Any, TYPE_CHECKING

from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._manga_user_subscription import manga_user_subscription
from .base_manga_notify_model import BaseMangaNotifyModel

if TYPE_CHECKING:
    from . import Chapter, UserSubscription


class Manga(BaseMangaNotifyModel):
    __tablename__ = "manga"

    uuid = mapped_column(VARCHAR(36), primary_key=True)
    language_code = mapped_column(VARCHAR(15), nullable=False, primary_key=True)
    title = mapped_column(VARCHAR(255), nullable=False)

    chapters: Mapped[list[Chapter]] = relationship("Chapter", back_populates="manga", cascade="all, delete")
    subscribed_users: Mapped[list[UserSubscription]] = relationship(
        "UserSubscription",
        secondary=manga_user_subscription,
        back_populates="subscribed_mangas"
    )

    def __init__(self, *, uuid: str, language_code: str, title: str, **kw: Any):
        self.uuid = uuid
        self.language_code = language_code
        self.title = title
        super().__init__(**kw)
