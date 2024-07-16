from .._base_mysql_database import BaseMySQLDatabase
from .model.base_manga_notify_model import BaseMangaNotifyModel
from .repository import *


class MangaNotifyDatabase(BaseMySQLDatabase):

    def __init__(self, user: str, password: str, host: str, port: int, database: str) -> None:
        super().__init__(user, password, host, port, database)
        self._base_model = BaseMangaNotifyModel()

        self._guild_subscription_repository = GuildSubscriptionRepository(self)
        self._manga_repository = MangaRepository(self)
        self._user_subscription_repository = UserSubscriptionRepository(self)

        self.repositories.extend([
            self.guild_subscription_repository,
            self.manga_repository,
            self.user_subscription_repository,
        ])

        self._manga_user_subscription_association = MangaUserSubscriptionAssociation(
            self, self.manga_repository, self.user_subscription_repository
        )

    @property
    def guild_subscription_repository(self):
        return self._guild_subscription_repository

    @property
    def manga_repository(self):
        return self._manga_repository

    @property
    def user_subscription_repository(self):
        return self._user_subscription_repository

    @property
    def manga_user_subscription_association(self):
        return self._manga_user_subscription_association

    @property
    def base_model(self) -> BaseMangaNotifyModel:
        return self._base_model
