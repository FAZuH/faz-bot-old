from fazbot.db.manga_notify.repository import *

from ._common_manga_notify_repository_test import CommonMangaNotifyRepositoryTest


class TestUserSubscriptionRepository(CommonMangaNotifyRepositoryTest.Test[UserSubscriptionRepository]):

    # override
    def _get_mock_data(self):
        model = self.repo.model

        # 1: mock data
        mock_data1 = model(user_id=1, is_notify=True)
        # 2: duplicate of 1
        mock_data2 = mock_data1.clone()
        # 3: duplicate with different primary key of 1
        mock_data3 = mock_data1.clone()
        mock_data3.user_id = 2
        # 4: duplicate with different non-primary key of 1
        mock_data4 = mock_data1.clone()
        mock_data4.is_notify = False
        return (mock_data1, mock_data2, mock_data3, mock_data4, "is_notify")

    # override
    @property
    def repo(self):
        return self.database.user_subscription_repository
