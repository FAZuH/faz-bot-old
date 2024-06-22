# pyright: basic
from unittest import TestCase
from unittest.mock import MagicMock

from fazbot.bot.invoke import InvokeCraftedProbability


class TestCraftedProbability(TestCase):

    def setUp(self) -> None:
        self.image_asset = MagicMock()
        InvokeCraftedProbability.__View = MagicMock
        InvokeCraftedProbability.ASSET_CRAFTINGTABLE = self.image_asset
        return super().setUp()

    def test_run(self) -> None:
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

