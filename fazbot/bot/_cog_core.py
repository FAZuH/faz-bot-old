from __future__ import annotations

from typing import TYPE_CHECKING

from .cog import Admin, Help, Info, WynnAnalyze, WynnStat, WynnTrack, WynnUtils
from .invoked import InvokedBase

if TYPE_CHECKING:
    from fazbot import Bot


class CogCore:

    def __init__(self, bot: Bot) -> None:
        self._bot = bot

    async def setup(self) -> None:
        self._admin = Admin(self._bot)
        self._help = Help(self._bot)
        self._info = Info(self._bot)
        self._wynn_analyze = WynnAnalyze(self._bot)
        self._wynn_stat = WynnStat(self._bot)
        self._wynn_track = WynnTrack(self._bot)
        self._wynn_utils = WynnUtils(self._bot)
        self._bot.client.add_all_application_commands()
        self._bot.core.logger.console_logger.info("Added all application commands.")

    def load_assets(self) -> None:
        self._bot.core.asset.load()
        InvokedBase.set_asset(self._bot.core.asset)
