from uuid import UUID

from fazbot.db.fazdb.repository.guild_member_history_repository import (
    GuildMemberHistoryRepository,
)

from ._common_fazdb_repository_test import CommonFazdbRepositoryTest


class TestGuildMemberHistoryRepository(CommonFazdbRepositoryTest.Test[GuildMemberHistoryRepository]):

    # override
    def _get_mock_data(self):
        model = self.repo.model

        uuid1 = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea200").bytes
        uuid2 = UUID("33c3ad56-5e9b-4bfe-9685-9fc4df2a67fa").bytes
        mock_data1 = model(
            uuid=uuid1, contributed=1, joined=self._get_mock_datetime(), datetime=self._get_mock_datetime()
        )
        mock_data2 = mock_data1.clone()
        mock_data3 = mock_data1.clone()
        del mock_data3.unique_id
        mock_data3.uuid = uuid2
        mock_data3 = mock_data3.clone()
        mock_data4 = mock_data1.clone()
        mock_data4.contributed = 2
        return (mock_data1, mock_data2, mock_data3, mock_data4, "contributed")

    # override
    @property
    def repo(self):
        return self.database.guild_member_history_repository
