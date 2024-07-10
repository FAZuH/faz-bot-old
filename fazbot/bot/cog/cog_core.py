from __future__ import annotations
from typing import Iterable, TYPE_CHECKING

from . import Admin, Help, Info, WynnAnalyze, WynnStat, WynnTrack, WynnUtils
from ._cog_base import CogBase

if TYPE_CHECKING:
    from .. import Bot


class CogCore:

    def __init__(self, bot: Bot) -> None:
        self._bot = bot
        self._cogs: list[CogBase] = []

        self.admin = Admin(self._bot)
        self.help = Help(self._bot)
        self.info = Info(self._bot)
        self.wynn_analyze = WynnAnalyze(self._bot)
        self.wynn_stat = WynnStat(self._bot)
        self.wynn_track = WynnTrack(self._bot)
        self.wynn_utils = WynnUtils(self._bot)

        self._cogs.append(self.admin)
        self._cogs.append(self.help)
        self._cogs.append(self.info)
        self._cogs.append(self.wynn_analyze)
        self._cogs.append(self.wynn_stat)
        self._cogs.append(self.wynn_track)
        self._cogs.append(self.wynn_utils)

    async def setup(self, whitelisted_guild_ids: Iterable[int]) -> None:
        """Intansiates all cogs and adds all application commands to the client.
        Should only be run once, that is, during start up"""
        for cog in self._cogs:
            cog.setup(whitelisted_guild_ids)
