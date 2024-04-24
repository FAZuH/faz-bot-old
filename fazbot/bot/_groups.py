from __future__ import annotations
from typing import TYPE_CHECKING

from .command_group import (
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


class Groups:

    def __init__(self, bot: Bot, app: App) -> None:
        self._bot = bot
        self._app = app

    def setup(self, guilds: list[Guild]) -> None:
        args = (self._bot, self._app, guilds)

        self._admin = Admin(*args)
        self._help = Help(*args)
        self._info = Info(*args)
        self._wynn_analyze = WynnAnalyze(*args)
        self._wynn_stat = WynnStat(*args)
        self._wynn_track = WynnTrack(*args)
        self._wynn_utils = WynnUtils(*args)

        self._admin.setup()
        self._help.setup()
        self._info.setup()
        self._wynn_analyze.setup()
        self._wynn_stat.setup()
        self._wynn_track.setup()
        self._wynn_utils.setup()
