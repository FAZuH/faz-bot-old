from __future__ import annotations
from typing import TYPE_CHECKING, Any

import discord
from discord.ext import commands

from .. import Utils
from fazbot.enum import UserdataFile

from . import CogBase

if TYPE_CHECKING:
    from discord.ext import commands


class Admin(CogBase):

    def _setup(self) -> None:
        self.admin.add_check(self._bot.checks.is_admin)

    @commands.hybrid_group(description="Admin commands.")
    async def admin(self, ctx: commands.Context[Any]) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid command.")

    @admin.command(description="Bans an user from using the bot.")
    async def ban(self, ctx: commands.Context[Any], user_id: str) -> None:
        user_id_ = await Utils.parse_big_int(ctx, user_id)
        if not user_id_:
            return
        user = self._bot.bot.get_user(user_id_)
        if not user:
            await ctx.send(f"Uer with ID `{user_id}` not found.")
            return
        banned_users = self._app.userdata.get(UserdataFile.BANNED_USERS)
        if user_id_ in banned_users:
            await ctx.send(f"User `{user.name}` (`{user.id}`) is already banned.")
            return
        banned_users.append(user_id_)  # type: ignore
        self._app.userdata.save(UserdataFile.BANNED_USERS)
        await ctx.send(f"Banned user `{user.name}` (`{user.id}`).")

    @admin.command()
    async def unban(self, ctx: commands.Context[Any], user_id: str) -> None:
        user_id_ = await Utils.parse_big_int(ctx, user_id)
        if not user_id_:
            return
        user = self._bot.bot.get_user(user_id_)
        if not user:
            await ctx.send(f"User with ID `{user_id}` not found.")
            return
        banned_users = self._app.userdata.get(UserdataFile.BANNED_USERS)
        if user_id_ not in banned_users:
            await ctx.send(f"User `{user.name}` (`{user.id}`) is not banned.")
            return
        banned_users.remove(user_id_)  # type: ignore
        self._app.userdata.save(UserdataFile.BANNED_USERS)
        await ctx.send(f"Unbanned user `{user.name}` (`{user.id}`).")

    @admin.command(description="Echoes a message.")
    async def echo(self, ctx: commands.Context[Any], message: str) -> None:
        await ctx.send(message)

    @admin.command(description="Reloads asset.")
    async def reload_asset(self, ctx: commands.Context[Any]) -> None:
        self._app.asset.load()
        await ctx.send("Reloaded asset successfully.")

    @admin.command(description="Reloads configs.")
    async def reload_config(self, ctx: commands.Context[Any]) -> None:
        self._app.config.load()
        await ctx.send("Reloaded config successfully.")

    @admin.command(description="Reloads userdata.")
    async def reload_userdata(self, ctx: commands.Context[Any]) -> None:
        self._app.userdata.load()
        await ctx.send("Reloaded userdata successfully.")

    @admin.command(description="Sends a message to a channel.")
    async def send(self, ctx: commands.Context[Any], channel_id: str, message: str) -> None:
        channel_id_ = await Utils.parse_big_int(ctx, channel_id)
        if not channel_id_:
            return
        channel = self._bot.bot.get_channel(channel_id_)
        if not hasattr(channel, "send"):
            await ctx.send(f"Channel of type `{type(channel)}` does not support sending messages.")
            return

        try:
            await channel.send(message)  # type: ignore
        except discord.DiscordException as e:
            await ctx.send(f"Failed to send message: {e}")
        await ctx.send(f"Sent message on channel `{channel.name}` (`{channel.id}`).")  # type: ignore

    @admin.command(description="Synchronizes commands with Discord for a guild.")
    async def sync_guild(self, ctx: commands.Context[Any], guild_id: str) -> None:
        guild_id_ = await Utils.parse_big_int(ctx, guild_id)
        if not guild_id_:
            return
        guild = self._bot.bot.get_guild(guild_id_)
        if not guild:
            await ctx.send(f"Guild with ID `{guild_id_}` not found.")
            return

        await self._bot.bot.tree.sync(guild=guild)
        await ctx.send(f"Synchronized app commands for guild `{guild.name}` (`{guild.id}`).")

    @admin.command(description="Synchronizes commands with Discord.")
    async def sync(self, ctx: commands.Context[Any]) -> None:
        guilds_len = 0
        for guild in self._bot.synced_guilds:
            await self._bot.bot.tree.sync(guild=guild)
            guilds_len += 1
        await ctx.send(f"Synchronized app commands across {guilds_len} guilds.")

    @admin.command(description="Shuts down the bot.")
    async def shutdown(self, ctx: commands.Context[Any]) -> None:
        await ctx.send("Shutting down...")
        self._bot.stop()

    @admin.command(description="Whispers a message to a user.")
    async def whisper(self, ctx: commands.Context[Any], user_id: str, message: str) -> None:
        user_id_ = await Utils.parse_big_int(ctx, user_id)
        if not user_id_:
            return

        user = self._bot.bot.get_user(user_id_)
        if not user:
            await ctx.send(f"Guild with ID `{user_id}` not found.")
            return
        try:
            await user.send(message)
        except discord.DiscordException as e:
            await ctx.send(f"Failed to whisper message: `{e}`")
        await ctx.send(f"Whispered message to `{user.name}` (`{user.id}`).")
