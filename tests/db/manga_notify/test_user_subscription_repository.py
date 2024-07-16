from typing import override

from sqlalchemy.engine import mock
from fazbot.db.manga_notify.repository import *

from ._common_manga_notify_repository_test import CommonMangaNotifyRepositoryTest


class TestUserSubscriptionRepository(CommonMangaNotifyRepositoryTest.Test[UserSubscriptionRepository]):

    async def test_insert_and_delete_subscribed_manga(self) -> None:
        entity = self.repo.model(id=1, name='.fazuh', guild_id=921720674823839804)
        await self.database.manga_repository.insert(self.manga)
        await self.repo.insert(entity)

        # Insert manga to user_subscription.subscribed_mangas
        async with self.database.enter_async_session() as ses:
            entity = await self.repo.select(1, session=ses)
            assert entity
            mangas = await entity.awaitable_attrs.subscribed_mangas
            self.assertEqual(entity.id, 1)
            self.assertEqual(len(mangas), 0)
            mangas.append(self.manga)

        # Remove manga to user_subscription.subscribed_mangas
        async with self.database.enter_async_session() as ses:
            entity = await self.repo.select(1, session=ses)
            assert entity
            mangas = await entity.awaitable_attrs.subscribed_mangas
            # Verify insertion
            self.assertEqual(entity.id, 1)
            self.assertEqual(len(mangas), 1)
            self.assertEqual(mangas[0].uuid, '46596dea-95de-40e8-b2b8-4e63aa6acd1a')
            mangas.remove(self.manga)

        # Verify removal
        async with self.database.enter_async_session() as ses:
            entity = await self.repo.select(1, session=ses)
            assert entity
            mangas = await entity.awaitable_attrs.subscribed_mangas
            self.assertEqual(entity.id, 1)
            self.assertEqual(len(mangas), 0)

    @override
    async def asyncSetUp(self) -> None:
        ret = await super().asyncSetUp()
        guild_model = self.database.guild_subscription_repository.model
        self.guild_subscription = guild_model(
            id=921720674823839804,
            name='pwr',
            channel_id=1262078950402691132,
            channel_name='manga_updates',
            is_notify=True
        )
        mock_guild = guild_model(id=1, name='a', channel_id=1, channel_name='b', is_notify=True)
        await self.database.guild_subscription_repository.insert([ self.guild_subscription, mock_guild ])
        self.manga = self.database.manga_repository.model(
            uuid='46596dea-95de-40e8-b2b8-4e63aa6acd1a',
            language_code='en',
            title='The Magical Revolution of the Reincarnated Princess and the Genius Young Lady'
        )
        return ret

    @override
    def _get_mock_data(self):
        model = self.repo.model

        # 1: mock data
        mock_data1 = model(id=1, name='a', guild_id=1, is_notify=False, is_notify_guild=False)
        # 2: duplicate of 1
        mock_data2 = mock_data1.clone()
        # 3: duplicate with different primary key of 1
        mock_data3 = mock_data1.clone()
        mock_data3.id = 2
        # 4: duplicate with different non-primary key of 1
        mock_data4 = mock_data1.clone()
        mock_data4.name = 'b'
        return (mock_data1, mock_data2, mock_data3, mock_data4, "name")

    @property
    @override
    def repo(self):
        return self.database.user_subscription_repository
