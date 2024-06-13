import unittest
from unittest.mock import MagicMock

from fazbot.db.fazbot.model import BannedUser


class TestBannedUser(unittest.TestCase):

    def setUp(self) -> None:
        self.obj_userid = 12345
        self.obj_reason = "test"
        self.obj_from = MagicMock()
        self.obj_until = MagicMock()
        self.obj = BannedUser(self.obj_userid, self.obj_reason, self.obj_from, self.obj_until)
        return super().setUp()

    def test_to_dict(self) -> None:
        # ACT
        dict_ = self.obj.to_dict()

        # ASSERT
        self.assertEqual(dict_["user_id"], self.obj_userid)
        self.assertEqual(dict_["reason"], self.obj_reason)
        self.assertEqual(dict_["from"], self.obj_from)
        self.assertEqual(dict_["until"], self.obj_until)

    def test_from_dict(self) -> None:
        # PREPARE
        data = {
            "user_id": self.obj_userid,
            "reason": self.obj_reason,
            "from": self.obj_from,
            "until": self.obj_until
        }

        # ACT
        obj = BannedUser.from_dict(data)

        # ASSERT
        self.assertEqual(obj.user_id, self.obj_userid)
        self.assertEqual(obj.reason, self.obj_reason)
        self.assertEqual(obj.from_, self.obj_from)
        self.assertEqual(obj.until, self.obj_until)

