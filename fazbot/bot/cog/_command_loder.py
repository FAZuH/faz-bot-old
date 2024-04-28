
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generator

from discord.ext.commands.hybrid import HybridAppCommand, HybridCommand

if TYPE_CHECKING:
    from discord import Guild
    from discord.ext import commands

    from fazbot import Core


class CommandLoader:

    def __init__(self, app: Core, cog: commands.Cog, guilds: list[Guild]) -> None:
        self._app = app
        self._cog = cog
        self._guilds = guilds

    def _walk_hybrid_app_commands(self) -> Generator[HybridAppCommand[commands.Cog, ..., Any], None, None]:
        for cmd in self._cog.walk_commands():
            if isinstance(cmd, HybridCommand) and cmd.app_command:
                yield cmd.app_command

    def load_commands(self) -> None:
        """ Loads commands defined on the cog, and adds the. """
        cmds = {*self._walk_hybrid_app_commands(), *self._cog.walk_app_commands()}
        for cmd in cmds:
            self._app.bot.bot.tree.add_command(cmd, guilds=self._guilds, override=True)
            self._app.logger.console_logger.info(f"Added app command: {cmd.qualified_name}")
