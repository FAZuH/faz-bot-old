# pyright: reportMissingTypeStubs=false
from __future__ import annotations
from typing import TYPE_CHECKING, Any

from discord.ext import commands

from . import CogBase

if TYPE_CHECKING:
    from discord.ext.commands import Context


class Admin(CogBase):

    @commands.hybrid_command(name="echo", description="Echoes a message.")
    async def _echo(self, ctx: Context[Any], message: str) -> None:
        await ctx.send(message)

    @commands.hybrid_command(name="reload_config", description="Reloads configs.")
    async def _reload_config(self, ctx: Context[Any]) -> None:
        self._app.config.load_config()
        await ctx.send("Reloaded config successfully.")

    @commands.hybrid_command(name="sync", description="Resynchronizes commands with Discord.")
    async def _sync(self, ctx: Context[Any]) -> None:
        guilds_len = 0
        for guild in self._bot.synced_guilds:
            self._app.logger.console_logger.debug(f"Synchronizing commands for guild {guild.name} ({guild.id}).")
            cmds = await self._bot.bot.tree.sync(guild=guild)
            self._app.logger.console_logger.success(f"Synchronized {len(cmds)} commands in {guild.name} ({guild.id}).")
            guilds_len += 1

        await ctx.send(f"Synchronized app commands across {guilds_len}.")

    @commands.hybrid_command(name="shutdown", description="Shuts down the bot.")
    async def _shutdown(self, ctx: Context[Any]) -> None:
        await ctx.send("Shutting down...")
        self._bot.stop()
