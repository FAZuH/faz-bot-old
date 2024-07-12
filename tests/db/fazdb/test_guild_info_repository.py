from uuid import UUID

from fazbot.db.fazdb.repository.guild_info_repository import GuildInfoRepository

from ._common_fazdb_repository_test import CommonFazdbRepositoryTest


class TestGuildInfoRepository(CommonFazdbRepositoryTest.Test[GuildInfoRepository]):

    # override
    def _get_mock_data(self):
        model = self.repo.model

        uuid1 = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea200").bytes
        uuid2 = UUID("33c3ad56-5e9b-4bfe-9685-9fc4df2a67fa").bytes
        mock_data1 = model(name='a', prefix='b', created=self._get_mock_datetime(), uuid=uuid1)
        mock_data2 = mock_data1.clone()
        mock_data3 = mock_data1.clone()
        mock_data3.uuid = uuid2
        mock_data4 = mock_data1.clone()
        mock_data4.prefix = 'c'
        return (mock_data1, mock_data2, mock_data3, mock_data4, "prefix")

    # override
    @property
    def repo(self):
        return self.database.guild_info_repository
