from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands

from . import CommandLoader

if TYPE_CHECKING:
    from discord import Guild

    from fazbot import Bot, Core


class GroupCogBase(commands.GroupCog):

    def __init__(self, bot: Bot, app: Core, guilds: list[Guild]) -> None:
        self._bot = bot
        self._app = app
        self._guilds = guilds
        self._base_cog = CommandLoader(app, self, guilds)

        self._setup()
        self._base_cog.load_commands()

    def _setup(self) -> None:
        """ Method to be run on cog initialization. Override this method in subclasses. """
        pass
