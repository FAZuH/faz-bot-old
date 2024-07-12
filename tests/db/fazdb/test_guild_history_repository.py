from fazbot.db.fazdb.repository.guild_history_repository import GuildHistoryRepository

from ._common_fazdb_repository_test import CommonFazdbRepositoryTest


class TestGuildHistoryRepository(CommonFazdbRepositoryTest.Test[GuildHistoryRepository]):

    # override
    def _get_mock_data(self):
        model = self.repo.model

        mock_data1 = model(
            name="a", level=1.0, territories=1, wars=1, member_total=1,
            online_members=1, datetime=self._get_mock_datetime()
        )
        mock_data2 = mock_data1.clone()
        mock_data3 = mock_data1.clone()
        del mock_data3.unique_id
        mock_data3.name = "b"
        mock_data3 = mock_data3.clone()
        mock_data4 = mock_data1.clone()
        mock_data4.level = 2.0
        return (mock_data1, mock_data2, mock_data3, mock_data4, "level")

    # override
    @property
    def repo(self):
        return self.database.guild_history_repository
