from fazbot.db.fazdb.repository.fazdb_uptime_repository import FazdbUptimeRepository

from ._common_fazdb_repository_test import CommonFazdbRepositoryTest


class TestFazdbUptimeRepository(CommonFazdbRepositoryTest.Test[FazdbUptimeRepository]):

    # override
    def _get_mock_data(self):
        model = self.repo.model

        mock_data1 = model(
            start_time=self._get_mock_datetime().replace(day=1),
            stop_time=self._get_mock_datetime().replace(day=2)
        )
        mock_data2 = mock_data1.clone()
        mock_data3 = mock_data1.clone()
        mock_data3.start_time = self._get_mock_datetime().replace(day=3, microsecond=0)
        mock_data4 = mock_data1.clone()
        mock_data4.stop_time = self._get_mock_datetime().replace(day=3, microsecond=0)
        return (mock_data1, mock_data2, mock_data3, mock_data4, "stop_time")

    # override
    @property
    def repo(self):
        return self.database.fazdb_uptime_repository
