from copy import deepcopy
from datetime import datetime, timedelta
from typing import Any

from fazbot.db.fazbot.model import WhitelistedGuild
from ._common_repository_test import CommonRepositoryTest


class TestWhitelistedGuildRepository(CommonRepositoryTest.Test[WhitelistedGuild, int]):

    async def test_get_all_whitelisted_guilds_ids_return_value(self) -> None:
        test_data1 = self.test_data
        test_data2 = deepcopy(test_data1)
        test_data2.guild_id = 2
        test_data3 = deepcopy(test_data1)
        test_data3.guild_id = 3

        test_guild_ids = [test_data1.guild_id, test_data2.guild_id, test_data3.guild_id]

        await self.repo.insert((test_data1, test_data2, test_data3))

        guild_ids = await self.repo.get_all_whitelisted_guilds()

        self.assertListEqual(guild_ids, test_guild_ids)

    # override
    def get_data(self):
        self.guild_id = 1
        self.guild_name = "test"
        self.from_ = datetime.now().replace(microsecond=0)
        self.until = self.from_ + timedelta(days=1)
        test_data = self.model_cls(guild_id=self.guild_id, guild_name=self.guild_name, from_=self.from_, until=self.until)
        return test_data

    # override
    @property
    def primary_key_value(self) -> Any:
        return self.guild_id

    # override
    @property
    def repo(self):
        return self.database.whitelisted_guild_repository

