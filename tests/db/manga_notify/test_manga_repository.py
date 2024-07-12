import uuid

from fazbot.db.manga_notify.repository import *

from ._common_manga_notify_repository_test import CommonMangaNotifyRepositoryTest


class TestMangaRepository(CommonMangaNotifyRepositoryTest.Test[MangaRepository]):

    # override
    def _get_mock_data(self):
        model = self.repo.model

        uuid1 = str(uuid.uuid4()).replace('-', '')
        uuid2 = str(uuid.uuid4()).replace('-', '')
        # 1: mock data
        mock_data1 = model(uuid=uuid1, language_code='en', title='a')
        # 2: duplicate of 1
        mock_data2 = mock_data1.clone()
        # 3: duplicate with different primary key of 1
        mock_data3 = mock_data1.clone()
        mock_data3.uuid = uuid2
        # 4: duplicate with different non-primary key of 1
        mock_data4 = mock_data1.clone()
        mock_data4.title = 'b'
        return (mock_data1, mock_data2, mock_data3, mock_data4, "title")

    # override
    @property
    def repo(self):
        return self.database.manga_repository
