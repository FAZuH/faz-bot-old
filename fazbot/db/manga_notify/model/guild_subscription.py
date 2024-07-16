from __future__ import annotations
from typing import Any, TYPE_CHECKING

from sqlalchemy.dialects.mysql import BIGINT, BOOLEAN, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_manga_notify_model import BaseMangaNotifyModel

if TYPE_CHECKING:
    from . import UserSubscription


class GuildSubscription(BaseMangaNotifyModel):
    __tablename__ = "guild_subscription"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(64), nullable=False)
    channel_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    channel_name: Mapped[str] = mapped_column(VARCHAR(64), nullable=False)
    is_notify: Mapped[bool] = mapped_column(BOOLEAN, nullable=False, default=False)

    subscribed_users: Mapped[list[UserSubscription]] = relationship(
        "UserSubscription",
        back_populates="guild_subscription",
        # lazy='selectin'
    )
    # One-to-many with UserSubscription

    def __init__(self, *, id: int, name: str, channel_id: int, channel_name: str, is_notify: bool = False, **kw: Any):
        self.id = id
        self.name = name
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.is_notify = is_notify
        super().__init__(**kw)

    def get_users_to_ping(self, manga_uuid: str) -> set[int]:
        """
        Get a set of user IDs who have notifications enabled and are subscribed to a specific manga.

        Args:
            manga_uuid (str): The UUID of the manga to check for user subscriptions.

        Returns:
            set[int]: A set of user IDs who should be pinged for the given manga.
        """
        users_to_ping: set[int] = set()
        for user in self.subscribed_users:
            if not user.is_notify or not user.is_notify_guild:
                continue

            try:
                is_user_subscribed = user.is_subscribed_manga(manga_uuid)
            except ValueError:
                continue

            if is_user_subscribed:
                users_to_ping.add(user.id)
        return users_to_ping
