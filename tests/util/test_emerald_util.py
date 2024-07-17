from unittest import TestCase

from fazbot.wynn import EmeraldUtil, Emeralds


class TestEmeraldUtil(TestCase):

    def test_crafted_util(self) -> None:
        # ASSERT
        set_price_tm, set_price_silverbull = EmeraldUtil.get_set_price(Emeralds.from_string("100eb"))
        self.assertEqual(set_price_tm.total, 6094)
        self.assertEqual(set_price_silverbull.total, 6212)
