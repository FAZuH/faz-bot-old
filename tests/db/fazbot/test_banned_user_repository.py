from fazbot.db.fazbot.repository.banned_user_repository import BannedUserRepository

from ._common_fazbot_repository_test import CommonFazbotRepositoryTest


class TestBannedUserRepository(CommonFazbotRepositoryTest.Test[BannedUserRepository]):

    # override
    def _get_mock_data(self):
        model = self.repo.get_model_cls()

        mock_data1 = model(user_id=1, reason='a', from_=self._get_mock_datetime(), until=self._get_mock_datetime())
        mock_data2 = mock_data1.clone()
        mock_data3 = mock_data1.clone()
        mock_data3.user_id = 2
        mock_data4 = mock_data1.clone()
        mock_data4.reason = 'b'
        return (mock_data1, mock_data2, mock_data3, mock_data4, "reason")

    # override
    @property
    def repo(self):
        return self.database.banned_user_repository
