# pyright: basic
from decimal import Decimal
from unittest import TestCase
from unittest.mock import MagicMock

from fazbot.bot.command import IngredientProbability


class TestIngredientProbability(TestCase):

    def setUp(self) -> None:
       self._type = IngredientProbability

    async def test_run(self) -> None:
        intr = MagicMock()
        obj = self._type(intr, "1/1000", 500, 100)
        await obj.run()
        intr.assert_called_once()

    def test_parse_base_chance(self) -> None:
        test1 = self._type._parse_base_chance("10%")
        self.assertEqual(test1, Decimal(10))

        test2 = self._type._parse_base_chance("10.5%")
        self.assertEqual(test2, Decimal("10.5"))

        test3 = self._type._parse_base_chance("1/100")
        self.assertEqual(test3, Decimal(1) / Decimal(100))

        test4 = self._type._parse_base_chance("1.5/100")
        self.assertEqual(test4, Decimal("0.015"))

        test5 = self._type._parse_base_chance("1/100.5")
        self.assertEqual(test5, Decimal(1) / Decimal("100.5"))

        test6 = self._type._parse_base_chance("0.1")
        self.assertEqual(test6, Decimal("0.1"))

    def tearDown(self) -> None:
        pass
