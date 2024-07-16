from fazbot.db.fazdb.repository.worlds_repository import WorldsRepository

from ._common_fazdb_repository_test import CommonFazdbRepositoryTest


class TestWorldsRepository(CommonFazdbRepositoryTest.Test[WorldsRepository]):

    async def test_update_worlds_successful(self) -> None:
        """Test if worlds_repository.update_worlds() properly update worlds.
        Deletes worlds that's not up anymore, and updates player_count for worlds that's still up

        1. Insert with mock data: wc1, wc3
        2. update_worlds(wc2, wc3) mock data:
          - WC1 went down
          - WC2 went up
          - WC3 stays the same
        3. Assert
          - WC1 no longer on table
          - WC2 is on table
          - WC3 player_count is updated
        """
        mock_data = self._get_mock_data()
        wc1 = mock_data[0]
        wc2 = mock_data[2]
        wc3 = wc2.clone()
        wc3.name = "WC3"
        await self.repo.insert([wc1, wc3])
        
        wc3_future = wc3.clone()
        wc3_future.player_count = 40
        await self.repo.update_worlds([wc2, wc3_future])

        rows = await self.repo.select_all()

        self.assertEqual(len(rows), 2)
        self.assertNotIn(wc1, rows)
        self.assertIn(wc2, rows)
        for row in rows:
            if row.name != wc3.name:  # type: ignore
                continue
            self.assertEqual(wc3_future.player_count, row.player_count)  # type: ignore

    # override
    def _get_mock_data(self):
        model = self.repo.model

        mock_data1 = model(name="WC1", player_count=50, time_created=self._get_mock_datetime().replace(day=1))
        mock_data2 = mock_data1.clone()
        mock_data3 = mock_data1.clone()
        mock_data3.name = "WC2"
        mock_data4 = mock_data1.clone()
        mock_data4.player_count = 49
        # mock_data4.time_created = datetime.now().replace(microsecond=0)
        return (mock_data1, mock_data2, mock_data3, mock_data4, "player_count")

    # override
    @property
    def repo(self):
        return self.database.worlds_repository
