from __future__ import annotations
from typing import TYPE_CHECKING

from . import Admin, Help, Info, WynnAnalyze, WynnStat, WynnTrack, WynnUtils, CogBase

if TYPE_CHECKING:
    from fazbot import Bot


class CogCore:

    def __init__(self, bot: Bot) -> None:
        self._bot = bot
        self._cogs: list[CogBase] = []

    def setup(self, whitelisted_guild_ids: list[int]) -> None:
        """Intansiates all cogs and adds all application commands to the client.
        Should only be run once"""
        CogBase.set_whitelisted_guild_ids(whitelisted_guild_ids)

        self._cogs.append(Admin(self._bot))
        self._cogs.append(Help(self._bot))
        self._cogs.append(Info(self._bot))
        self._cogs.append(WynnAnalyze(self._bot))
        self._cogs.append(WynnStat(self._bot))
        self._cogs.append(WynnTrack(self._bot))
        self._cogs.append(WynnUtils(self._bot))

        self._bot.client.add_all_application_commands()

        with self._bot.core.enter_logger() as logger:
            logger.console.info("Added all application commands.")
