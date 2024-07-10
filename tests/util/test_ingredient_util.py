from decimal import Decimal
from unittest import TestCase

from fazbot.wynn import IngredientUtil


class TestIngredientUtil(TestCase):

    def test_ingredient_util(self) -> None:
        # PREPARE
        ingutil = IngredientUtil(Decimal(0.1), 50, 50)
        # ASSERT
        self.assertEqual(ingutil.base_probability, Decimal(0.1))
        self.assertEqual(ingutil.loot_quality, 50)
        self.assertEqual(ingutil.loot_bonus, 50)
        self.assertEqual(ingutil.loot_boost, 100)
        self.assertAlmostEqual(ingutil.boosted_probability, Decimal(0.2))
