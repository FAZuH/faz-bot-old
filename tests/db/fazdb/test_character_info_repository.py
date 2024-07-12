from uuid import UUID

from fazbot.db.fazdb.repository import CharacterInfoRepository

from ._common_fazdb_repository_test import CommonFazdbRepositoryTest


class TestCharacterInfoRepository(CommonFazdbRepositoryTest.Test[CharacterInfoRepository]):

    # override
    def _get_mock_data(self):
        model = self.repo.model

        chuuid1 = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea200").bytes
        chuuid2 = UUID("33c3ad56-5e9b-4bfe-9685-9fc4df2a67fa").bytes
        uuid = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea201").bytes
        mock_data1 = model(character_uuid=chuuid1, uuid=uuid, type='ARCHER')
        mock_data2 = mock_data1.clone()
        mock_data3 = mock_data1.clone()
        mock_data3.character_uuid = chuuid2
        mock_data4 = mock_data1.clone()
        mock_data4.type = 'ASSASSIN'
        return (mock_data1, mock_data2, mock_data3, mock_data4, "type")

    # override
    @property
    def repo(self):
        return self.database.character_info_repository
