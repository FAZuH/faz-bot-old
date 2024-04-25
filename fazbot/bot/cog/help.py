from __future__ import annotations
from typing import Any

from discord.app_commands import Command
from discord.ext import commands

from ..command import Help as HelpCommand
from . import CogBase


class Help(CogBase):

    @commands.hybrid_command(name="help", description="Help command")
    async def _help(self, ctx: commands.Context[Any]) -> None:
        cmds = [
                cmd for cmd in self._bot.bot.tree.get_commands(guild=ctx.guild)
                if isinstance(cmd, Command)
        ]
        await HelpCommand(ctx, cmds).run()
