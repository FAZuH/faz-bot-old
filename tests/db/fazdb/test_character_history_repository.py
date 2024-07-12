from uuid import UUID

from fazbot.db.fazdb.repository import CharacterHistoryRepository

from ._common_fazdb_repository_test import CommonFazdbRepositoryTest


class TestCharacterHistoryRepository(CommonFazdbRepositoryTest.Test[CharacterHistoryRepository]):

    # override
    def _get_mock_data(self):
        uuid1 = UUID("b30f5e97-957d-47f6-bf1e-9e48d9fea200").bytes
        uuid2 = UUID("33c3ad56-5e9b-4bfe-9685-9fc4df2a67fa").bytes

        model = self.repo.model
        mock_data1 = model(
            character_uuid=uuid1, level=1, xp=1, wars=1, playtime=1.0,
            mobs_killed=1, chests_found=1, logins=1, deaths=1, discoveries=1,
            hardcore=False, ultimate_ironman=False, ironman=False, craftsman=False,
            hunted=False, alchemism=1.0, armouring=1.0, cooking=1.0, jeweling=1.0,
            scribing=1.0, tailoring=1.0, weaponsmithing=1.0, woodworking=1.0,
            mining=1.0, woodcutting=1.0, farming=1.0, fishing=1.0, dungeon_completions=1,
            quest_completions=1, raid_completions=1, datetime=self._get_mock_datetime(),
        )
        mock_data2 = mock_data1.clone()
        mock_data3 = mock_data1.clone()
        del mock_data3.unique_id
        mock_data3.character_uuid = uuid2
        mock_data3 = mock_data3.clone()
        mock_data4 = mock_data1.clone()
        mock_data4.level = 2
        return (mock_data1, mock_data2, mock_data3, mock_data4, "level")

    # override
    @property
    def repo(self):
        return self.database.character_history_repository
