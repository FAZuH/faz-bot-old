from __future__ import annotations
from asyncio import subprocess
from datetime import datetime
import subprocess
from typing import Any, Iterable

import nextcord
from nextcord import Interaction

from . import CogBase
from .. import Utils, CommandFailure


class Admin(CogBase):

    # override
    def _setup(self, whitelisted_guild_ids: Iterable[int]) -> None:
        for app_cmd in self.application_commands:
            # app_cmd.guild_ids.add(dev_server_id)
            app_cmd.add_guild_rollout(self._bot.core.config.dev_server_id)
            self._bot.client.add_application_command(app_cmd, overwrite=True, use_rollout=True)

    # override
    def cog_application_command_check(self, interaction: Interaction[Any]):  # type: ignore
        return self._bot.checks.is_admin(interaction)

    @nextcord.slash_command(name="admin", description="Admin commands.")
    async def admin(self, interaction: Interaction[Any]) -> None: ...
  
    @admin.subcommand(name="ban")
    async def ban(
            self,
            interaction: Interaction[Any],
            user_id: str,
            reason: str = '',
            until: str | None = None
        ) -> None:
        """(dev only) Bans an user from using the bot.

        Parameters
        ----------
        user_id : str
            The user ID to ban.
        reason : str, optional
            Reason of ban, by default ''
        until : str | None, optional
            Time when the user will be unbanned, by default None
        """
        user = await Utils.must_get_user(self._bot.client, user_id)

        async with self._enter_db_session() as (db, session):
            banlist = db.banned_user_repository
            model_cls = banlist.get_model_cls()

            if await banlist.is_exists(user.id, session):
                raise CommandFailure(f"User `{user.name}` (`{user.id}`) is already banned.")

            user_to_ban = model_cls(
                user_id=user.id,
                reason=reason,
                from_=datetime.now(),
                until=Utils.must_parse_date_string(until) if until else None
            )

            await banlist.insert(user_to_ban)

        await self._respond_successful(interaction, f"Banned user `{user.name}` (`{user.id}`).")

    @admin.subcommand(name="unban")
    async def unban(self, interaction: Interaction[Any], user_id: str) -> None:
        """(dev only) Unbans an user from using the bot.

        Parameters
        ----------
        user_id : str
            The user ID to unban.
        """
        user = await Utils.must_get_user(self._bot.client, user_id)

        async with self._enter_db_session() as (db, session):
            banlist = db.banned_user_repository

            if not await banlist.is_exists(user.id, session):
                raise CommandFailure(f"User `{user.name}` (`{user.id}`) is not banned.")

            await banlist.delete(user.id, session)
            
        await self._respond_successful(interaction, f"Unbanned user `{user.name}` (`{user.id}`).")

    @admin.subcommand(name="echo")
    async def echo(self, interaction: Interaction[Any], message: str) -> None:
        """(dev only) Echoes a message.

        Parameters
        ----------
        message : str
            The message to echo.
        """
        await interaction.send(message)

    @admin.subcommand(name="reload_asset")
    async def reload_asset(self, interaction: Interaction[Any]) -> None:
        """(dev only) Reloads asset."""
        self._bot.core.asset.read_all()

        self._bot.asset_manager.load_assets()
        await self._respond_successful(interaction, "Reloaded asset successfully.")

    @admin.subcommand(name="reload_config")
    async def reload_config(self, interaction: Interaction[Any]) -> None:
        """(dev only) Reloads configs."""
        self._bot.core.config.read()

        await self._respond_successful(interaction, "Reloaded config successfully.")

    @admin.subcommand(name="send")
    async def send(self, interaction: Interaction[Any], channel_id: str, message: str) -> None:
        """(dev only) Unbans an user from using the bot.

        Parameters
        ----------
        channel_id : str
            The channel ID to send the message.
        message : str
            Message to send.
        """
        channel = await Utils.must_get_channel(self._bot.client, channel_id)

        if not self.__is_channel_sendable(channel):
            raise CommandFailure(f"Channel of type `{type(channel)}` does not support sending messages.") 

        try:
            await channel.send(message)  # type: ignore
        except nextcord.DiscordException as e:
            raise CommandFailure(f"Failed sending message: {e}")

        await self._respond_successful(interaction, f"Sent message on channel `{channel.name}` (`{channel.id}`).")  # type: ignore

    @admin.subcommand(name="sync_guild")
    async def sync_guild(self, interaction: Interaction[Any], guild_id: str) -> None:
        """(dev only) Syncs app commands for a specific guild.

        Parameters
        ----------
        guild_id : str
            The guild ID to sync app commands to.
        """        
        await interaction.response.defer()
        guild = await Utils.must_get_guild(self._bot.client, guild_id)

        await self._bot.client.sync_application_commands(guild_id=guild.id)

        synced_app_cmds = 0
        for app_cmd in self._bot.client.get_all_application_commands():
            if guild.id in app_cmd.guild_ids:
                synced_app_cmds += 1

        await self._respond_successful(
            interaction,
            f"Synchronized {synced_app_cmds} app commands for guild `{guild.name}` `({guild.id})`."
        )

    @admin.subcommand(name="sync")
    async def sync(self, interaction: Interaction[Any]) -> None:
        """(dev only) Synchronizes all app commands with Discord."""
        await interaction.response.defer()
        await self._bot.client.sync_all_application_commands()
        await self._respond_successful(interaction, f"Synchronized app commands.")

    @admin.subcommand(name="shutdown", description="Shuts down the bot.")
    async def shutdown(self, interaction: Interaction[Any]) -> None:
        """(dev only) Shutdowns the bot enitirely."""
        await self._respond_successful(interaction, "Shutting down...")
        self._bot.stop()

    @admin.subcommand(name="whisper")
    async def whisper(self, interaction: Interaction[Any], user_id: str, message: str) -> None:
        """(dev only) Whispers a message to a user.

        Parameters
        ----------
        user_id : str
            The user ID to whisper.
        message : str
            The message to whisper to the user.
        """
        user = await Utils.must_get_user(self._bot.client, user_id)

        try:
            await user.send(message)
        except nextcord.DiscordException as e:
            raise CommandFailure(f"Failed whispering message to user {user.display_name}: `{e}`")

        await self._respond_successful(interaction, f"Whispered message to `{user.name}` (`{user.id}`).")

    # TODO: manage syncing database and local memory
    @admin.subcommand(name="whitelist")
    async def whitelist(self, interaction: Interaction[Any], guild_id: str, until: str | None = None) -> None:
        """(dev only) Whitelists or unwhitelists a guild from using the bot.

        Parameters
        ----------
        guild_id : str
            The guild ID to whitelist.
        until : str | None, optional
            Date until the whitelist expires, by default None
        """
        guild = await Utils.must_get_guild(self._bot.client, guild_id)

        async with self._enter_db_session() as (db, session):
            whitelist = db.whitelisted_guild_repository
            model_cls = whitelist.get_model_cls()

            if await whitelist.is_exists(guild.id, session):
                raise CommandFailure(f"Guild `{guild.name}` (`{guild.id}`) is already whitelisted.")

            guild_to_whitelist = model_cls(
                guild_id=guild.id,
                guild_name=guild.name,
                from_=datetime.now(),
                until=Utils.must_parse_date_string(until) if until else None
            )
            
            await whitelist.insert(guild_to_whitelist, session)
            
        await self._respond_successful(interaction, f"Whitelisted guild `{guild.name}` (`{guild.id}`).")

    @admin.subcommand(name="unwhitelist")
    async def unwhitelist(self, interaction: Interaction[Any], guild_id: str) -> None:
        """(dev only) Unwhitelists a guild from using the bot.

        Parameters
        ----------
        guild_id : str
            The guild ID to unwhitelist.
        """
        guild = await Utils.must_get_guild(self._bot.client, guild_id)

        async with self._enter_db_session() as (db, session):
            whitelist = db.whitelisted_guild_repository

            if not await whitelist.is_exists(guild.id, session):
                raise CommandFailure(f"Guild `{guild.name}` (`{guild.id}`) is not whitelisted.")

            await whitelist.delete(guild.id, session) 

        await self._respond_successful(interaction, f"Unwhitelisted guild `{guild.name}` (`{guild.id}`).")

    @admin.subcommand(name="execute")
    async def execute(self, interaction: Interaction[Any], command: str) -> None:
        """(dev only) Execute `command` directly to the host device.

        Parameters
        ----------
        command : str
            The command to execute.
        """
        command_ = command.split(' ')
        result = subprocess.run(command_, capture_output=True, text=True)

        if result.returncode == 0:
            success_msg = (
                "Command executed successfully!\n"
                "Output:\n"
                f"{result.stdout}"
            )
            await self._respond_successful(interaction, success_msg)
        else:
            err_msg = (
                "Error executing command.\n"
                "Error message:\n"
                f"{result.stderr}"
            )
            raise CommandFailure(err_msg)

    def __is_channel_sendable(self, channel: object) -> bool:
        return hasattr(channel, "send")
