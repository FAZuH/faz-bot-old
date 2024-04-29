from typing import Any

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from fazbot.enum import UserdataFile

from . import CogBase
from .. import Utils


class Admin(CogBase):

    # @override
    def _setup(self) -> None:
        # Admin check for application commands.
        self.admin.add_check(self._bot.checks.is_admin)
        for subcmd in self.admin.children.values():
            # Admin check for admin subcommands.
            subcmd.add_check(self._bot.checks.is_admin)

    # @override
    def bot_check(self, ctx: commands.Context[Any]) -> bool:
        # Admin check for context commands.
        return self._bot.checks.is_admin(ctx)

    @nextcord.slash_command(name="admin", description="Admin commands.")
    async def admin(self, interaction: Interaction[Any]) -> None:
        pass

    @admin.subcommand(name="ban", description="Bans an user from using the bot.")
    async def ban(self, interaction: Interaction[Any], user_id: str) -> None:
        user_id_ = await Utils.parse_big_int(interaction, user_id)
        if not user_id_:
            return
        user = self._bot.bot.get_user(user_id_)
        if not user:
            await interaction.response.send_message(f"User with ID `{user_id}` not found.")
            return
        banned_users = self._app.userdata.get(UserdataFile.BANNED_USERS)
        if user_id_ in banned_users:
            await interaction.response.send_message(f"User `{user.name}` (`{user.id}`) is already banned.")
            return
        banned_users.append(user_id_)  # type: ignore
        self._app.userdata.save(UserdataFile.BANNED_USERS)
        await interaction.response.send_message(f"Banned user `{user.name}` (`{user.id}`).")

    @admin.subcommand(name="unban", description="Unbans an user from using the bot.")
    async def unban(self, interaction: Interaction[Any], user_id: str) -> None:
        user_id_ = await Utils.parse_big_int(interaction, user_id)
        if not user_id_:
            return
        user = self._bot.bot.get_user(user_id_)
        if not user:
            await interaction.response.send_message(f"User with ID `{user_id}` not found.")
            return
        banned_users = self._app.userdata.get(UserdataFile.BANNED_USERS)
        if user_id_ not in banned_users:
            await interaction.response.send_message(f"User `{user.name}` (`{user.id}`) is not banned.")
            return
        banned_users.remove(user_id_)  # type: ignore
        self._app.userdata.save(UserdataFile.BANNED_USERS)
        await interaction.response.send_message(f"Unbanned user `{user.name}` (`{user.id}`).")

    @admin.subcommand(name="echo", description="Echoes a message.")
    async def echo(self, interaction: Interaction[Any], message: str) -> None:
        await interaction.response.send_message(message)

    @admin.subcommand(name="reload_asset", description="Reloads asset.")
    async def reload_asset(self, interaction: Interaction[Any]) -> None:
        self._app.asset.load()
        await interaction.response.send_message("Reloaded asset successfully.")

    @admin.subcommand(name="reload_config", description="Reloads configs.")
    async def reload_config(self, interaction: Interaction[Any]) -> None:
        self._app.config.load()
        await interaction.response.send_message("Reloaded config successfully.")

    @admin.subcommand(name="reload_userdata", description="Reloads userdata.")
    async def reload_userdata(self, interaction: Interaction[Any]) -> None:
        self._app.userdata.load()
        await interaction.response.send_message("Reloaded userdata successfully.")

    @admin.subcommand(name="send", description="Sends a message to a channel.")
    async def send(self, interaction: Interaction[Any], channel_id: str, message: str) -> None:
        channel_id_ = await Utils.parse_big_int(interaction, channel_id)
        if not channel_id_:
            return
        channel = self._bot.bot.get_channel(channel_id_)
        if not hasattr(channel, "send"):
            await interaction.response.send_message(f"Channel of type `{type(channel)}` does not support sending messages.")
            return

        try:
            await channel.send(message)  # type: ignore
        except nextcord.DiscordException as e:
            await interaction.response.send_message(f"Failed to send message: {e}")
        await interaction.response.send_message(f"Sent message on channel `{channel.name}` (`{channel.id}`).")  # type: ignore

    @commands.command(name="sync_guild", description="Synchronizes app commands for a specific guild.")
    async def sync_guild(self, ctx: commands.Context[Any], guild_id: str) -> None:
        try:
            guild_id_ = int(guild_id)
        except ValueError:
            await ctx.send(f"Failed parsing {guild_id} into an integer.")
            return
        if not guild_id_:
            return
        guild = self._bot.bot.get_guild(guild_id_)
        if not guild:
            await ctx.send(f"Guild with ID `{guild_id_}` not found.")
            return
        await self._bot.bot.sync_application_commands(guild_id=guild.id)
        await ctx.send(f"Synchronized app commands for guild `{guild.name}` (`{guild.id}`).")

    @commands.command(name="sync", description="Synchronizes app commands across all whitelisted guilds.")
    async def sync(self, ctx: commands.Context[Any]) -> None:
        guilds_len = 0
        for guild in self._bot.synced_guilds:
            await self._bot.bot.sync_application_commands(guild_id=guild.id)
            guilds_len += 1
        await ctx.send(f"Synchronized app commands across {guilds_len} guilds.")

    @admin.subcommand(name="shutdown", description="Shuts down the bot.")
    async def shutdown(self, interaction: Interaction[Any]) -> None:
        await interaction.response.send_message("Shutting down...")
        self._bot.stop()

    @admin.subcommand(name="whisper", description="Whispers a message to a user.")
    async def whisper(self, interaction: Interaction[Any], user_id: str, message: str) -> None:
        user_id_ = await Utils.parse_big_int(interaction, user_id)
        if not user_id_:
            return

        user = self._bot.bot.get_user(user_id_)
        if not user:
            await interaction.response.send_message(f"Guild with ID `{user_id}` not found.")
            return
        try:
            await user.send(message)
        except nextcord.DiscordException as e:
            await interaction.response.send_message(f"Failed to whisper message: `{e}`")
        await interaction.response.send_message(f"Whispered message to `{user.name}` (`{user.id}`).")
