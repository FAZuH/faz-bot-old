import unittest
from unittest.mock import MagicMock

from fazbot.bot.invoke import InvokeCraftedProbability


class TestCraftedProbability(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.image_asset = MagicMock()
        InvokeCraftedProbability._View = MagicMock
        InvokeCraftedProbability.ASSET_CRAFTINGTABLE = self.image_asset
        return super().setUp()

    async def test_run(self) -> None:
        interaction = MagicMock()
        ing_strs = [
            "1,2,50",
            "1,2,50",
            "1,2,50",
            "1,2,50"
        ]
        craftedprob = InvokeCraftedProbability(interaction, ing_strs)
        for ing in craftedprob._craftutil.ingredients:
            self.assertEqual(ing.min_value, 1)
            self.assertEqual(ing.max_value, 2)
            self.assertEqual(ing.boost, 50)

