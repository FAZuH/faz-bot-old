from __future__ import annotations

from typing import TYPE_CHECKING

from nextcord.ext import commands

if TYPE_CHECKING:
    from nextcord import Guild

    from fazbot import Bot, Core


class CogBase(commands.Cog):

    def __init__(self, bot: Bot, app: Core, guilds: list[Guild]) -> None:
        self._bot = bot
        self._app = app
        self._guilds = guilds
        self.setup()

    def setup(self) -> None:
        self._setup()
        for cmd in self.application_commands:
            for guild in self._guilds:
                cmd.add_guild_rollout(guild=guild)
        self._bot.bot.add_cog(self)
        self._app.logger.console_logger.info(f"Added cog {self.__class__.__qualname__} to client.")

    def _setup(self) -> None:
        """ Method to be run on cog initialization. Override this method in subclasses. """
        pass
