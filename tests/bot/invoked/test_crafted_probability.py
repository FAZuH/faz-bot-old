# pyright: basic
from unittest import TestCase
from unittest.mock import MagicMock

from fazbot.bot.invoked import CraftedProbability


class TestCraftedProbability(TestCase):

    def test_run(self) -> None:
        interaction = MagicMock(bytes)
        image_asset = MagicMock()
        CraftedProbability._asset = image_asset
        ing_strs = [
            "1,2,50",
            "1,2,50",
            "1,2,50",
            "1,2,50"
        ]
        craftedprob = CraftedProbability(interaction, ing_strs)
        for ing in craftedprob._craftutil.ingredients:
            self.assertEqual(ing.min_value, 1)
            self.assertEqual(ing.max_value, 2)
            self.assertEqual(ing.boost, 50)
