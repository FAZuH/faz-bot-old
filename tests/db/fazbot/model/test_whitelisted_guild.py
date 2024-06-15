from unittest import TestCase

import sqlalchemy as sa

from fazbot.db.fazbot.model import WhitelistedGuild 


class TestWhitelistedGuild(TestCase):

    def test_column_types(self) -> None:
        self.assertTrue(WhitelistedGuild.guild_id.primary_key)
        self.assertIsInstance(WhitelistedGuild.guild_id, sa.Integer)

        self

