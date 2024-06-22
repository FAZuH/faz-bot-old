from __future__ import annotations
from typing import TYPE_CHECKING

from nextcord.types.interactions import ApplicationCommandType

from . import Admin, Help, Info, WynnAnalyze, WynnStat, WynnTrack, WynnUtils, CogBase

if TYPE_CHECKING:
    from fazbot import Bot


class CogCore:

    def __init__(self, bot: Bot) -> None:
        self._bot = bot
        self._cogs: list[CogBase] = []

    async def setup(self, whitelisted_guild_ids: list[int]) -> None:
        """Intansiates all cogs and adds all application commands to the client.
        Should only be run once"""
        CogBase.set_whitelisted_guild_ids(whitelisted_guild_ids)

        self._admin = Admin(self._bot)
        self._help = Help(self._bot)
        self._info = Info(self._bot)
        self._wynn_analyze = WynnAnalyze(self._bot)
        self._wynn_stat = WynnStat(self._bot)
        self._wynn_track = WynnTrack(self._bot)
        self._wynn_utils = WynnUtils(self._bot)

        self._cogs.append(self._admin)
        self._cogs.append(self._help)
        self._cogs.append(self._info)
        self._cogs.append(self._wynn_analyze)
        self._cogs.append(self._wynn_stat)
        self._cogs.append(self._wynn_track)
        self._cogs.append(self._wynn_utils)

        self.__setup_all_cogs()

        self._bot.client.add_all_application_commands()
        application_commands = self._bot.client.get_all_application_commands()
        self._bot.logger.console.info(
            f"Loaded {len(application_commands)} application commands "
            f"across {len(whitelisted_guild_ids)} guilds."
        )

        await self.__sync_dev_guild()

    def __setup_all_cogs(self) -> None:
        for cog in self._cogs:
            cog.setup()

    async def __sync_dev_guild(self) -> None:
        dev_server_id = self._bot.core.config.dev_server_id
        await self._bot.client.sync_application_commands(guild_id=dev_server_id)
