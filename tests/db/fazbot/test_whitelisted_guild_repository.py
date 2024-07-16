from loguru import logger
from fazbot.db.fazbot.repository import WhitelistedGuildRepository

from ._common_fazbot_repository_test import CommonFazbotRepositoryTest


class TestWhitelistedGuildRepository(CommonFazbotRepositoryTest.Test[WhitelistedGuildRepository]):

    async def test_get_all_whitelisted_guilds_ids_return_value(self) -> None:
        mock_data = self._get_mock_data()
        to_insert = mock_data[0], mock_data[2]

        await self.repo.insert(to_insert)

        guild_ids = set(await self.repo.get_all_whitelisted_guild_ids())
        self.assertSetEqual(guild_ids, {guild.guild_id for guild in to_insert})
        
    # override
    def _get_mock_data(self):
        model = self.repo.model

        mock_data1 = model(guild_id=1, guild_name='a', from_=self._get_mock_datetime(), until=self._get_mock_datetime())
        mock_data2 = mock_data1.clone()
        mock_data3 = mock_data1.clone()
        mock_data3.guild_id = 2
        mock_data4 = mock_data1.clone()
        mock_data4.guild_name = 'b'

        return (mock_data1, mock_data2, mock_data3, mock_data4, "guild_name")


    # override
    @property
    def repo(self):
        return self.database.whitelisted_guild_repository
