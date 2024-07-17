from typing import override

from fazbot.db.fazbot.repository import WhitelistGroupRepository

from ._common_fazbot_repository_test import CommonFazbotRepositoryTest


class TestWhitelistGroupRepository(CommonFazbotRepositoryTest.Test[WhitelistGroupRepository]):

    async def test_ban_user(self) -> None:
        await self.repo.ban_user(1)  # act
        # assert: user is successfully banned
        all = await self.repo.select_all()
        ids = [e.id for e in all]
        self.assertIn(1, ids)
        
    async def test_unban_user(self) -> None:
        await self.repo.ban_user(1)  # prepare
        await self.repo.unban_user(1)  # act
        # assert: user is succesfully banned
        all = await self.repo.select_all()
        self.assertEqual(len(all), 0)

    async def test_is_banned_user(self) -> None:
        is_ban = await self.repo.is_banned_user(1)  # act
        self.assertFalse(is_ban)  # assert: is_ban returns false when user is not banned

        await self.repo.ban_user(1)  # prepare
        is_ban = await self.repo.is_banned_user(1)  # act
        self.assertTrue(is_ban)  # assert: is_ban returns true when user is banned

    async def test_whitelist_guild(self) -> None:
        await self.repo.whitelist_guild(1)  # act

        # assert: guild is successfully whitelisted
        all = await self.repo.select_all()
        ids = [e.id for e in all]
        self.assertIn(1, ids)
        
    async def test_unwhitelist_guild(self) -> None:
        await self.repo.ban_user(1)  # prepare
        await self.repo.unwhitelist_guild(1)  # act

        # assert: guild is succesfully unwhitelisted
        all = await self.repo.select_all()
        self.assertTrue(len(all), 0)

    async def test_is_whitelist_guild(self) -> None:
        is_ban = await self.repo.is_whitelisted_guild(1)  # act
        self.assertFalse(is_ban)  # assert: is_ban returns false when user is not banned

        await self.repo.whitelist_guild(1)  # prepare
        is_ban = await self.repo.is_whitelisted_guild(1)  # act
        self.assertTrue(is_ban)  # assert: is_ban returns true when user is banned

    async def test_get_all_whitelisted_guild_ids(self) -> None:
        # prepare
        ids_to_insert = (1, 2, 3)
        for id in ids_to_insert:
            await self.repo.whitelist_guild(id)
        # assert: get_all_whitelisted_guild_ids return value is correct
        ids = tuple(await self.repo.get_all_whitelisted_guild_ids())
        self.assertTupleEqual(ids, ids_to_insert)

    @override
    def _get_mock_data(self):
        model = self.repo.model
        mock_data1 = model(id=1, type='a', reason='a', from_=self._get_mock_datetime(), until=self._get_mock_datetime())
        mock_data2 = mock_data1.clone()
        mock_data3 = mock_data1.clone()
        mock_data3.id = 2
        mock_data4 = mock_data1.clone()
        mock_data4.reason = 'b'
        return (mock_data1, mock_data2, mock_data3, mock_data4, "reason")

    @property
    @override
    def repo(self):
        return self.database.whitelist_group_repository
