from .._base_mysql_database import BaseMySQLDatabase
from .model.base_manga_notify_model import BaseMangaNotifyModel
from .repository import *


class MangaNotifyDatabase(BaseMySQLDatabase):

    def __init__(self, user: str, password: str, host: str, port: int, database: str) -> None:
        super().__init__(user, password, host, port, database)
        self._base_model = BaseMangaNotifyModel()

        self._chapter_repository = ChapterRepository(self)
        self._manga_repository = MangaRepository(self)
        # self._notification_history_repository = NotificationHistoryRepository(self)
        self._user_subscription_repository = UserSubscriptionRepository(self)

        self.repositories.extend([
            self.chapter_repository,
            self.manga_repository,
            # self.notification_history_repository,
            self.user_subscription_repository,
        ])

    @property
    def chapter_repository(self):
        return self._chapter_repository

    @property
    def manga_repository(self):
        return self._manga_repository

    # @property
    # def notification_history_repository(self):
    #     return self._notification_history_repository

    @property
    def user_subscription_repository(self):
        return self._user_subscription_repository

    @property
    def base_model(self) -> BaseMangaNotifyModel:
        return self._base_model
