from __future__ import annotations

from typing import TYPE_CHECKING

from nextcord.ext import commands

if TYPE_CHECKING:
    from fazbot import Bot


class CogBase(commands.Cog):

    def __init__(self, bot: Bot) -> None:
        self._bot = bot
        self.setup()

    def setup(self) -> None:
        self._setup()
        for cmd in self.application_commands:
            for guild in self._bot.core.userdata.get(self._bot.core.userdata.enum.WHITELISTED_GUILDS):
                assert isinstance(guild, int)
                cmd.add_guild_rollout(guild=guild)
        self._bot.client.add_cog(self)
        self._bot.core.logger.console.info(f"Added cog {self.__class__.__qualname__} to client.")

    def _setup(self) -> None:
        """ Method to be run on cog initialization. Override this method in subclasses. """
        pass
