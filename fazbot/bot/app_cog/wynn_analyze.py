from __future__ import annotations
from typing import TYPE_CHECKING

from discord import app_commands

from . import CogBase

if TYPE_CHECKING:
    from discord import Interaction


class WynnAnalyze(CogBase):

    def _setup(self) -> None:
        self._commands.extend([

        ])

