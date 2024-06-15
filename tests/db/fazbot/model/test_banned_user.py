from datetime import datetime
from typing import Optional
from unittest import TestCase

from fazbot.db.fazbot.model import BannedUser



class TestBannedUser(TestCase):

    def test_column_types(self) -> None:
        self.assertIsInstance(BannedUser.user_id, int)
        self.assertIsInstance(BannedUser.reason, str)
        self.assertIsInstance(BannedUser.from_, datetime)
        self.assertIsInstance(BannedUser.until, Optional[datetime])        

