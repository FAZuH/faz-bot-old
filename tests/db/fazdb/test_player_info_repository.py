from uuid import UUID

from fazbot.db.fazdb.repository.player_info_repository import PlayerInfoRepository

from ._common_fazdb_repository_test import CommonFazdbRepositoryTest


class TestPlayerInfoRepository(CommonFazdbRepositoryTest.Test[PlayerInfoRepository]):

    # override
    def _get_mock_data(self):
        model = self.repo.model

        uuid1 = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea200").bytes
        uuid2 = UUID("33c3ad56-5e9b-4bfe-9685-9fc4df2a67fa").bytes
        mock_data1 = model(uuid=uuid1, latest_username='a', first_join=self._get_mock_datetime())
        mock_data2 = mock_data1.clone()
        mock_data3 = mock_data1.clone()
        mock_data3.uuid = uuid2
        mock_data4 = mock_data1.clone()
        mock_data4.latest_username = 'b'
        return (mock_data1, mock_data2, mock_data3, mock_data4, "latest_username")

    # override
    @property
    def repo(self):
        return self.database.player_info_repository
