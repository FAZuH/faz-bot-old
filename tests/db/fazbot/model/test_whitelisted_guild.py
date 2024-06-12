import unittest
from unittest.mock import MagicMock

from fazbot.db.fazbot.model import WhitelistedGuild


class TestWhitelistedGuild(unittest.TestCase):

    def setUp(self) -> None:
        self.obj_guildid = 12345
        self.obj_guildname = "test"
        self.obj_from = MagicMock()
        self.obj_until = MagicMock()
        self.obj = WhitelistedGuild(
            self.obj_guildid,
            self.obj_guildname,
            self.obj_from,
            self.obj_until
        )
        return super().setUp()

    def test_to_dict(self) -> None:
        # ACT
        dict_ = self.obj.to_dict()

        # ASSERT
        self.assertEqual(dict_["guild_id"], self.obj_guildid)
        self.assertEqual(dict_["guild_name"], self.obj_guildname)
        self.assertEqual(dict_["from"], self.obj_from)
        self.assertEqual(dict_["until"], self.obj_until)

    def test_from_dict(self) -> None:
        # PREPARE
        data = {
            "guild_id": self.obj_guildid,
            "guild_name": self.obj_guildname,
            "from": self.obj_from,
            "until": self.obj_until
        }

        # ACT
        obj = WhitelistedGuild.from_dict(data)

        # ASSERT
        self.assertEqual(obj.guild_id, self.obj_guildid)
        self.assertEqual(obj.guild_name, self.obj_guildname)
        self.assertEqual(obj.from_, self.obj_from)
        self.assertEqual(obj.until, self.obj_until)

