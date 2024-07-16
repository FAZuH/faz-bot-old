from __future__ import annotations
from typing import Any, TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import BIGINT, BOOLEAN, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._manga_user_subscription import manga_user_subscription
from .base_manga_notify_model import BaseMangaNotifyModel

if TYPE_CHECKING:
    from . import GuildSubscription, Manga


class UserSubscription(BaseMangaNotifyModel):
    __tablename__ = "user_subscription"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(64), nullable=False)
    is_notify: Mapped[bool] = mapped_column(BOOLEAN, nullable=False, default=False)
    is_notify_guild: Mapped[bool] = mapped_column(BOOLEAN, nullable=False, default=False)
    guild_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("guild_subscription.id"))

    guild_subscription: Mapped[GuildSubscription] = relationship(
        "GuildSubscription",
        back_populates="subscribed_users",
    )
    # Many-to-one with GuildSubscription
    subscribed_mangas: Mapped[list[Manga]] = relationship(
        "Manga",
        secondary=manga_user_subscription,
        back_populates="subscribed_users",
    )
    # Many-to-many with Manga through MangaUserSubscription

    def __init__(
            self,
            *,
            id: int,
            name: str,
            guild_id: int,
            is_notify: bool = False,
            is_notify_guild: bool = False,
            **kw: Any
        ):
        self.id = id
        self.name = name
        self.is_notify = is_notify
        self.is_notify_guild = is_notify_guild
        self.guild_id = guild_id
        super().__init__(**kw)

    def is_subscribed_manga(self, manga_uuid: str) -> bool:
        """
        Checks if the user is subscribed to a manga by its UUID.

        Args:
            manga_uuid (str): The UUID of the manga to check for subscription.

        Returns:
            bool: True if the user is subscribed to the manga, False otherwise.
        """
        for manga in self.subscribed_mangas:
            if manga.uuid == manga_uuid:
                return True
        return False
