from datetime import datetime, timedelta
from typing import Any

from fazbot.db.fazbot.model import WhitelistedGuild
from ._common_repository_test import CommonRepositoryTest


class TestWhitelistedGuildRepository(CommonRepositoryTest.Test[WhitelistedGuild, int]):

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

