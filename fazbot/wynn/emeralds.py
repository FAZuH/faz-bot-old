from __future__ import annotations
from math import floor
import re


class Emeralds:

    def __init__(self, emeralds: int = 0, blocks: int = 0, liquids: int = 0, stacks: int = 0) -> None:
        self._emeralds = emeralds
        self._blocks = blocks
        self._liquids = liquids
        self._stacks = stacks
        self._total = self._get_total(emeralds, blocks, liquids, stacks)

    def simplify(self) -> None:
        if self._emeralds >= 64:
            self._blocks += self._emeralds // 64
            self._emeralds %= 64

        if self._blocks >= 64:
            self._liquids += self._blocks // 64
            self._blocks %= 64

        if self._liquids >= 64:
            self._stacks += self._liquids // 64
            self._liquids %= 64

    @classmethod
    def from_string(cls, emerald_string: str) -> Emeralds:
        strings = emerald_string.split()
        if len(strings) == 1 and strings[0].isnumeric():
            return cls(emeralds=int(strings[0]))

        e = eb = le = stx = 0
        multiplier = 1
        for str_ in strings:
            input_split = re.match(r'^(.*?)([A-Za-z]+)$', str_)
            if not input_split:
                raise ValueError("Invalid emerald string.")
            amount = input_split.group(1)
            unit = input_split.group(2)

            parsed_amount = cls._parse_number_string(amount)
            if unit == 'e':
                e += int(parsed_amount)
            elif unit == 'eb':
                eb += int(parsed_amount)
            elif unit == 'le':
                le  += int(parsed_amount)
            elif unit == 'stx':
                stx += int(parsed_amount)
            elif unit == 'x':
                multiplier = parsed_amount
            else:
                raise ValueError(f"Invalid unit {unit} in emerald string.")

        total = floor(cls._get_total(e, eb, le, stx) * multiplier)
        return cls(emeralds=total)

    @property
    def total(self) -> int:
        return self._total

    @property
    def emeralds(self) -> int:
        return self._emeralds

    @property
    def blocks(self) -> int:
        return self._blocks

    @property
    def liquids(self) -> int:
        return self._liquids

    @property
    def stacks(self) -> int:
        return self._stacks


    @staticmethod
    def _get_total(emeralds: int, blocks: int, liquids: int, stacks: int) -> int:
        return emeralds + blocks * 64 + liquids * 64 * 64 + stacks * 64 * 64 * 64

    @staticmethod
    def _parse_number_string(number_string: str) -> float:
        if '/' in number_string:
            num, den = number_string.split('/')
            return int(num) / int(den)
        if '%' in number_string:
            return float(number_string.strip('%')) / 100
        return float(number_string)

    def __repr__(self) -> str:
        return f"{self._stacks}stx {self._liquids}le {self._blocks}eb {self._emeralds}e"

    def __eq__(self, other: Emeralds | int | str | object) -> bool:
        if isinstance(other, Emeralds):
            return self._total == other.total
        elif isinstance(other, int):
            return self._total == other
        elif isinstance(other, str):
            return str(self) == other
        return False

    def __add__(self, other: Emeralds | int) -> Emeralds:
        if isinstance(other, int):
            return Emeralds(emeralds=self._emeralds + other)
        return Emeralds(emeralds=self._emeralds + other.total)
