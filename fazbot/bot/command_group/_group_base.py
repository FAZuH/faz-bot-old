# pyright: reportMissingTypeStubs=false
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from discord.app_commands import Group

if TYPE_CHECKING:
    from discord import Guild
    from fazbot import App, Bot


class GroupBase(ABC):

    def __init__(self, bot: Bot, app: App, guilds: list[Guild]) -> None:
        self._bot = bot
        self._app = app
        self._guilds = guilds

    def _setup(self, group: Group) -> None:
        """
        Setup method to be called in setup() method on subclasses.
        Adds commands to self._command_tree.
        """
        self._bot.command_tree.add_command(group, guilds=self._guilds)
        self._app.logger.console_logger.info(f"Added command: {group.qualified_name}")

    @abstractmethod
    def setup(self) -> None: ...

