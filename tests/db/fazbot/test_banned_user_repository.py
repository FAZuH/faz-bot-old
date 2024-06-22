from datetime import datetime, timedelta

from fazbot.db.fazbot.model import BannedUser

from ._common_repository_test import CommonRepositoryTest


class TestBannedUserRepository(CommonRepositoryTest.Test[BannedUser, int]):

    # override
    def get_data(self):
        self.reason = "test"
        self.from_ = datetime.now().replace(microsecond=0)
        self.until = self.from_ + timedelta(days=1)

        self.user_id1 = 1
        self.user_id2 = 2
        self.user_id3 = 3

        test_data1 = self.model_cls(user_id=self.user_id1, reason=self.reason, from_=self.from_, until=self.until)
        test_data2 = self.model_cls(user_id=self.user_id2, reason=self.reason, from_=self.from_, until=self.until)
        test_data3 = self.model_cls(user_id=self.user_id3, reason=self.reason, from_=self.from_, until=self.until)

        test_data = (test_data1, test_data2, test_data3)
        return test_data

    # override
    @property
    def repo(self):
        return self.database.banned_user_repository
