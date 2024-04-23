from __future__ import annotations
from typing import TYPE_CHECKING

from .app_cog import (
    Admin,
    Help,
    Info,
    WynnAnalyze,
    WynnStat,
    WynnTrack,
    WynnUtils
)

if TYPE_CHECKING:
    from discord import  Guild
    from fazbot import App, Bot


class Cogs:

    def __init__(self, bot: Bot, app: App) -> None:
        self._bot = bot
        self._app = app

    def setup(self, guilds: list[Guild]) -> None:
        args = (self._bot, self._app)

        self._admin = Admin(*args)
        self._help = Help(*args)
        self._info = Info(*args)
        self._wynn_analyze = WynnAnalyze(*args)
        self._wynn_stat = WynnStat(*args)
        self._wynn_track = WynnTrack(*args)
        self._wynn_utils = WynnUtils(*args)

        self._admin.setup(guilds)
        self._help.setup(guilds)
        self._info.setup(guilds)
        self._wynn_analyze.setup(guilds)
        self._wynn_stat.setup(guilds)
        self._wynn_track.setup(guilds)
        self._wynn_utils.setup(guilds)
