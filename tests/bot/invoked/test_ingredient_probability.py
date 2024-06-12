# pyright: basic
from decimal import Decimal
from unittest import TestCase
from unittest.mock import MagicMock

from fazbot.bot.invoked import IngredientProbability


class TestIngredientProbability(TestCase):

    def setUp(self) -> None:
        self.interaction = MagicMock()
        self.obj = IngredientProbability(self.interaction, "1/1000", 500, 100)
        return super().setUp()

    async def test_run(self) -> None:
        await self.obj.run()
        self.interaction.assert_called_once()

    def test_parse_base_chance(self) -> None:
        test1 = self.obj._parse_base_chance("10%")
        self.assertAlmostEqual(test1, Decimal(0.1))

        test2 = self.obj._parse_base_chance("10.5%")
        self.assertAlmostEqual(test2, Decimal("0.105"))

        test3 = self.obj._parse_base_chance("1/100")
        self.assertAlmostEqual(test3, Decimal(1) / Decimal(100))

        test4 = self.obj._parse_base_chance("1.5/100")
        self.assertAlmostEqual(test4, Decimal("0.015"))

        test5 = self.obj._parse_base_chance("1/100.5")
        self.assertAlmostEqual(test5, Decimal(1) / Decimal("100.5"))

        test6 = self.obj._parse_base_chance("0.1")
        self.assertAlmostEqual(test6, Decimal("0.1"))

    def tearDown(self) -> None:
        pass
