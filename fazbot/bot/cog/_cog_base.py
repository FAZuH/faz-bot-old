# pyright: reportMissingTypeStubs=false
from __future__ import annotations
from typing import TYPE_CHECKING

from discord.ext.commands import Cog

if TYPE_CHECKING:
    from discord import Guild
    from fazbot import App, Bot


class CogBase(Cog):

    def __init__(self, bot: Bot, app: App, guilds: list[Guild]) -> None:
        self._bot = bot
        self._app = app
        self._guilds = guilds

    async def load_commands(self) -> None:
        """
        Setup method to be called in setup() method on subclasses.
        Adds commands to self._command_tree.
        """
        for cmd in self.walk_app_commands():
            self._bot.bot.tree.add_command(cmd, guilds=self._guilds)
            self._app.logger.console_logger.info(f"Added command: {cmd.qualified_name}")
        await self._bot.bot.add_cog(self)
