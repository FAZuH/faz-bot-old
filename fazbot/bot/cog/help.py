from __future__ import annotations
from typing import TYPE_CHECKING

from discord.app_commands import Command, command

from ..command import HelpCommand
from . import CogBase

if TYPE_CHECKING:
    from discord import Interaction


class Help(CogBase):

    @command(name="help", description="Help command")
    async def _help(self, interaction: Interaction) -> None:
        cmds = [
                cmd for cmd in self._bot.bot.tree.get_commands(guild=interaction.guild)
                if isinstance(cmd, Command)
        ]
        await HelpCommand(interaction, cmds).run()
