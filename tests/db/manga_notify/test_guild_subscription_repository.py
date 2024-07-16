from fazbot.db.manga_notify.repository import *

from ._common_manga_notify_repository_test import CommonMangaNotifyRepositoryTest


class TestGuildSubscriptionRepository(CommonMangaNotifyRepositoryTest.Test[GuildSubscriptionRepository]):

    # override
    def _get_mock_data(self):
        model = self.repo.model

        # 1: mock data
        mock_data1 = model(id=1, name='a', channel_id=1, channel_name='a', is_notify=False)
        # 2: duplicate of 1
        mock_data2 = mock_data1.clone()
        # 3: duplicate with different primary key of 1
        mock_data3 = mock_data1.clone()
        mock_data3.id = 2
        # 4: duplicate with different non-primary key of 1
        mock_data4 = mock_data1.clone()
        mock_data4.name = 'b'
        return (mock_data1, mock_data2, mock_data3, mock_data4, "name")

    # override
    @property
    def repo(self):
        return self.database.guild_subscription_repository
