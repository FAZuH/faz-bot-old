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

        self.admin = Admin(bot)
        self.help = Help(bot)
        self.info = Info(bot)
        self.wynn_analyze = WynnAnalyze(bot)
        self.wynn_stat = WynnStat(bot)
        self.wynn_track = WynnTrack(bot)
        self.wynn_utils = WynnUtils(bot)

        self._cogs.extend([
            self.admin,
            self.help,
            self.info,
            self.wynn_analyze,
            self.wynn_stat,
            self.wynn_track,
            self.wynn_utils
        ])

    async def setup(self, whitelisted_guild_ids: Iterable[int]) -> None:
        """Intansiates all cogs and adds all application commands to the client.
        Should only be run once, that is, during start up"""
        for cog in self._cogs:
            cog.setup(whitelisted_guild_ids)
