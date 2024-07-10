from decimal import Decimal
from math import floor

from .wynn_emeralds import WynnEmeralds


class EmeraldUtil:

    @staticmethod
    def get_set_price(emerald: WynnEmeralds) -> tuple[WynnEmeralds, WynnEmeralds]:
        set_price_tm = floor(emerald.total * Decimal(100 / 105)) - 1
        set_price_silverbull = floor(emerald.total * Decimal(100 / 103)) - 1
        return WynnEmeralds(set_price_tm), WynnEmeralds(set_price_silverbull)
