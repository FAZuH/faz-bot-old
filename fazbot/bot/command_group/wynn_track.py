from __future__ import annotations
from typing import TYPE_CHECKING

from discord.app_commands import Group

from . import GroupBase

if TYPE_CHECKING:
    from discord import Interaction


class WynnTrack(GroupBase, Group):

    def setup(self) -> None:
        Group.__init__(self)
        self._setup(self)
