from __future__ import annotations
from typing import TYPE_CHECKING

from discord.app_commands import Command, Group, command

from ..command import HelpCommand
from . import GroupBase

if TYPE_CHECKING:
    from discord import Interaction


class Help(GroupBase, Group):

    def setup(self) -> None:
        Group.__init__(self)
        self._setup(self)

    @command(name="help", description="Help command")
    async def _help(self, interaction: Interaction) -> None:
        cmds = [
                cmd for cmd in self._bot.command_tree.get_commands(guild=interaction.guild)
                if isinstance(cmd, Command)
        ]
        await HelpCommand(interaction, cmds).run()
