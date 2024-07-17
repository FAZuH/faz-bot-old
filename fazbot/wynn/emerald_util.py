from decimal import Decimal
from math import floor

from .emeralds import Emeralds


class EmeraldUtil:

    @staticmethod
    def get_set_price(emerald: Emeralds) -> tuple[Emeralds, Emeralds]:
        set_price_tm = floor(emerald.total * Decimal(100 / 105)) - 1
        set_price_silverbull = floor(emerald.total * Decimal(100 / 103)) - 1
        return Emeralds(set_price_tm), Emeralds(set_price_silverbull)
