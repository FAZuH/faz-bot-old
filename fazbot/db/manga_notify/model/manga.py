from __future__ import annotations
from typing import Any, TYPE_CHECKING

from hondana.types_.common import LanguageCode
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._manga_user_subscription import manga_user_subscription
from .base_manga_notify_model import BaseMangaNotifyModel

if TYPE_CHECKING:
    from . import UserSubscription


class Manga(BaseMangaNotifyModel):
    __tablename__ = "manga"

    uuid: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    language_code: Mapped[LanguageCode] = mapped_column(VARCHAR(8), primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)

    subscribed_users: Mapped[list[UserSubscription]] = relationship(
        "UserSubscription",
        secondary=manga_user_subscription,
        back_populates="subscribed_mangas",
    )
    # Many-to-many with UserSubscription through MangaUserSubscription

    def __init__(self, *, uuid: str, language_code: LanguageCode, title: str, **kw: Any):
        self.uuid = uuid
        self.language_code = language_code
        self.title = title
        super().__init__(**kw)

    def is_subscribed_user(self, user_id: int) -> bool:
        """
        Checks if the manga is being subscribed to a user by their user id.

        Args:
            user_id (str): The user id to check for subscription.

        Returns:
            bool: True if the manga is being subscribed to the user, False otherwise.
        """
        for user in self.subscribed_users:
            if user.id == user_id:
                return True
        return False
