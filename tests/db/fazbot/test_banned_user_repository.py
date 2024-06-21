from datetime import datetime, timedelta
from typing import Any

from fazbot.db.fazbot.model import BannedUser
from ._common_repository_test import CommonRepositoryTest


class TestBannedUserRepository(CommonRepositoryTest.Test[BannedUser, int]):

    # override
    def get_data(self):
        self.user_id = 1
        self.reason = "test"
        self.from_ = datetime.now().replace(microsecond=0)
        self.until = self.from_ + timedelta(days=1)
        test_data = self.model_cls(user_id=self.user_id, reason=self.reason, from_=self.from_, until=self.until)
        return test_data

    # override
    @property
    def primary_key_value(self) -> Any:
        return self.user_id

    # override
    @property
    def repo(self):
        return self.database.banned_user_repository
