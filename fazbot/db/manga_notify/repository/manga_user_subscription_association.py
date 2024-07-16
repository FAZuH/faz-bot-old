from __future__ import annotations
from typing import TYPE_CHECKING

from fazbot.db._base_mysql_database import BaseMySQLDatabase

if TYPE_CHECKING:
    from ..model import Manga, UserSubscription
    from . import MangaRepository, UserSubscriptionRepository


class MangaUserSubscriptionAssociation:

    def __init__(
            self,
            database: BaseMySQLDatabase,
            manga_repository: MangaRepository,
            user_subscription_repository: UserSubscriptionRepository
    ) -> None:
        self._database = database
        self._manga_repository = manga_repository
        self._user_subscription_repository = user_subscription_repository

    async def toggle(self, user: UserSubscription, manga: Manga) -> bool:
        user_repo = self.user_subscription_repository
        manga_repo = self.manga_repository

        await user_repo.insert(user, replace_on_duplicate=True)
        await manga_repo.insert(manga, replace_on_duplicate=True)

        async with self.database.enter_async_session() as ses:
            user_subs = await user_repo.select(user.id, session=ses)
            merged_user = await ses.merge(user_subs)
            merged_manga = await ses.merge(manga)

            assert merged_user and merged_manga
            await merged_user.awaitable_attrs.subscribed_mangas

            is_subscribed = merged_user.is_subscribed_manga(merged_manga.uuid)
            if is_subscribed:
                merged_user.subscribed_mangas.remove(merged_manga)
            else:
                merged_user.subscribed_mangas.append(merged_manga)

        return not is_subscribed

    @property
    def database(self):
        return self._database

    @property
    def manga_repository(self):
        return self._manga_repository

    @property
    def user_subscription_repository(self):
        return self._user_subscription_repository
