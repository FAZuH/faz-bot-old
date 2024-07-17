from decimal import Decimal
from unittest import TestCase

from fazbot.wynn import CraftedUtil, IngredientField


class TestCraftedUtil(TestCase):

    def test_crafted_util(self) -> None:
        # PREPARE
        ing1 = IngredientField(1, 2, 50)
        ing2 = IngredientField(1, 2, 50)
        ing3 = IngredientField(1, 2, 50)
        ing4 = IngredientField(1, 2, 50)
        craftedutil = CraftedUtil([ing1, ing2, ing3, ing4])

        # ASSERT
        self.assertEqual(4, craftedutil.crafted_roll_min)
        self.assertEqual(12, craftedutil.crafted_roll_max)
        self.assertEqual([ing1, ing2, ing3, ing4], craftedutil.ingredients)
        self.assertAlmostEqual(Decimal(0.060), craftedutil.craft_probs[4], delta=0.001)
        self.assertAlmostEqual(Decimal(0.245), craftedutil.craft_probs[6], delta=0.001)
        self.assertAlmostEqual(Decimal(0.375), craftedutil.craft_probs[8], delta=0.001)
        self.assertAlmostEqual(Decimal(0.255), craftedutil.craft_probs[10], delta=0.001)
        self.assertAlmostEqual(Decimal(0.065), craftedutil.craft_probs[12], delta=0.001)

