from __future__ import annotations
import re


class WynnEmeralds:

    def __init__(self, emeralds: int = 0, blocks: int = 0, liquids: int = 0, stacks: int = 0) -> None:
        self._emeralds = emeralds
        self._blocks = blocks
        self._liquids = liquids
        self._stacks = stacks
        self._compute_total()

    def simplify(self) -> None:
        self._compute_total()
        if self._emeralds > 64:
            self._blocks += self._emeralds // 64
            self._emeralds %= 64

        if self._blocks > 64:
            self._liquids += self._blocks // 64
            self._blocks %= 64

        if self._liquids > 64:
            self._stacks += self._liquids // 64
            self._liquids %= 64


    @classmethod
    def from_string(cls, emerald_string: str) -> WynnEmeralds:
        stx = re.findall(r'\b(\d+)stx\b', emerald_string)
        le = re.findall(r'\b(\d+)le\b', emerald_string)
        eb = re.findall(r'\b(\d+)eb\b', emerald_string)
        e = re.findall(r'\b(\d+)e\b', emerald_string)
        x = re.findall(r'\b(\d+)\bx\b', emerald_string)
        if len(x) > 1:
            raise ValueError("Max occurence of amount argument 'x' is once.")
        x = int(x[0]) if len(x) == 1 else 1
        try:
            ret = cls(
                    sum(map(int, e)),
                    sum(map(int, eb)),
                    sum(map(int, le)),
                    sum(map(int, stx)),
            )
        except ValueError as e:
            raise ValueError(f"An exception occured while trying to convert emerald string into integers: {e}.")
        return ret

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


    def _compute_total(self) -> None:
        self._total = self._emeralds + self._blocks * 64 + self._liquids * 64 * 64 + self._stacks * 64 * 64 * 64

    def __repr__(self) -> str:
        return f"{self._stacks}stx {self._liquids}le {self._blocks}eb {self._emeralds}e"

    def __eq__(self, other: WynnEmeralds | int | str | object) -> bool:
        if isinstance(other, WynnEmeralds):
            return self._total == other.total
        elif isinstance(other, int):
            return self._total == other
        elif isinstance(other, str):
            return str(self) == other
        return False

    def __add__(self, other: WynnEmeralds | int) -> WynnEmeralds:
        if isinstance(other, int):
            return WynnEmeralds(emeralds=self._emeralds + other)
        return WynnEmeralds(emeralds=self._emeralds + other.total)
