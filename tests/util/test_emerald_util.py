# pyright: basic
from decimal import Decimal
from unittest import TestCase

from fazbot.object import WynnEmeralds
from fazbot.util import EmeraldUtil


class TestEmeraldUtil(TestCase):

    def test_crafted_util(self) -> None:
        # ASSERT
        set_price_tm, set_price_silverbull = EmeraldUtil.get_set_price(WynnEmeralds.from_string("100eb"))
        self.assertEqual(set_price_tm.total, 6094)
        self.assertEqual(set_price_silverbull.total, 6212)
