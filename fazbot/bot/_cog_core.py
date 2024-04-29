from __future__ import annotations
from typing import TYPE_CHECKING

from .cog import (
    Admin,
    Help,
    Info,
    WynnAnalyze,
    WynnStat,
    WynnTrack,
    WynnUtils
)
from .invoked import InvokedBase

if TYPE_CHECKING:
    from nextcord import Guild
    from fazbot import Core, Bot


class CogCore:

    def __init__(self, bot: Bot, app: Core) -> None:
        self._bot = bot
        self._app = app

    async def setup(self, guilds: list[Guild]) -> None:
        args = (self._bot, self._app, guilds)
        self._admin = Admin(*args)
        self._help = Help(*args)
        self._info = Info(*args)
        self._wynn_analyze = WynnAnalyze(*args)
        self._wynn_stat = WynnStat(*args)
        self._wynn_track = WynnTrack(*args)
        self._wynn_utils = WynnUtils(*args)
        self._bot.bot.add_all_application_commands()
        self._app.logger.console_logger.info("Added all application commands.")

    def load_assets(self) -> None:
        self._app.asset.load()
        InvokedBase.set_asset(self._app.asset)
