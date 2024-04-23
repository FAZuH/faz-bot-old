from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING, Any

from discord.ext.commands import Cog

if TYPE_CHECKING:
    from discord import Guild
    from discord.app_commands import Command
    from fazbot import App, Bot


class CogBase(Cog):

    def __init__(self, bot: Bot, app: App) -> None:
        self._bot = bot
        self._app = app

        self._commands: list[Command[Any, ..., Any]] = []

    def setup(self, guilds: list[Guild]) -> None:
        """
        Setup method to be called after instantiation.
        Adds commands to self._command_tree.
        """
        self._setup()
        for cmd in self._commands:
            self._bot.command_tree.add_command(cmd, guilds=guilds)
            self._app.logger.console_logger.info(f"Added command: {cmd.name}")


    @abstractmethod
    def _setup(self) -> None:
        """ For subclasses to add commands into self._commands. """
        ...
