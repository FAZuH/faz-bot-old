from datetime import datetime, timedelta

from fazbot.db.fazbot.model import WhitelistedGuild

from ._common_repository_test import CommonRepositoryTest


class TestWhitelistedGuildRepository(CommonRepositoryTest.Test[WhitelistedGuild, int]):

    async def test_get_all_whitelisted_guilds_ids_return_value(self) -> None:
        test_guild_ids = set([guild.guild_id for guild in self.test_data])

        await self.repo.insert(self.test_data)

        guild_ids = set(await self.repo.get_all_whitelisted_guild_ids())
        self.assertSetEqual(guild_ids, test_guild_ids)
        
    # override
    def get_data(self):
        self.guild_name = "test"
        self.from_ = datetime.now().replace(microsecond=0)
        self.until = self.from_ + timedelta(days=1)

        self.guild_id1 = 1
        self.guild_id2 = 2
        self.guild_id3 = 3

        test_data1 = self.model_cls(guild_id=self.guild_id1, guild_name=self.guild_name, from_=self.from_, until=self.until)
        test_data2 = self.model_cls(guild_id=self.guild_id2, guild_name=self.guild_name, from_=self.from_, until=self.until)
        test_data3 = self.model_cls(guild_id=self.guild_id3, guild_name=self.guild_name, from_=self.from_, until=self.until)

        test_data = (test_data1, test_data2, test_data3)
        return test_data

    # override
    @property
    def repo(self):
        return self.database.whitelisted_guild_repository
