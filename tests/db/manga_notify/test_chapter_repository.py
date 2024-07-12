import uuid

from fazbot.db.manga_notify.repository import *

from ._common_manga_notify_repository_test import CommonMangaNotifyRepositoryTest


class TestChapterRepository(CommonMangaNotifyRepositoryTest.Test[ChapterRepository]):

    uuid1 = str(uuid.uuid4()).replace('-', '')
    uuid2 = str(uuid.uuid4()).replace('-', '')

    # override
    async def test_delete_successful(self) -> None:
        cls = self.__class__
        await self.database.manga_repository.delete_many([(cls.uuid1, 'en'), (cls.uuid2, 'en')])

        rows = await self._get_all_inserted_rows()
        self.assertEqual(len(rows), 0)

    # override
    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()
        cls = self.__class__
        manga_model = self.database.manga_repository.model

        mock_manga1 = manga_model(uuid=cls.uuid1, language_code='en', title='a')
        mock_manga2 = manga_model(uuid=cls.uuid2, language_code='en', title='b')
        await self.database.manga_repository.insert([mock_manga1, mock_manga2])

    # override
    def _get_mock_data(self):
        cls = self.__class__
        model = self.repo.model

        uuid3 = str(uuid.uuid4()).replace('-', '')
        uuid4 = str(uuid.uuid4()).replace('-', '')
        # 1: mock data
        mock_data1 = model(uuid=uuid3, manga_uuid=cls.uuid1)
        # 2: duplicate of 1
        mock_data2 = mock_data1.clone()
        # 3: duplicate with different primary key of 1
        mock_data3 = mock_data1.clone()
        mock_data3.uuid = uuid4
        # 4: duplicate with different non-primary key of 1
        mock_data4 = mock_data1.clone()
        mock_data4.manga_uuid = cls.uuid2
        return (mock_data1, mock_data2, mock_data3, mock_data4, "manga_uuid")

    # override
    @property
    def repo(self):
        return self.database.chapter_repository
