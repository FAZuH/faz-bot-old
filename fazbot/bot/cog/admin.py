from datetime import datetime
from typing import Any

import nextcord
from nextcord import Interaction

from . import CogBase
from .. import Utils


class Admin(CogBase):

    # @override
    def cog_application_command_check(self, interaction: Interaction[Any]) -> bool:
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
        """Bans an user from using the bot.

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

        with self._bot.core.enter_fazbotdb() as db:
            is_banned = await db.banned_user_repository.is_banned(user.id)
            if is_banned:
                return await self._respond_error(interaction, f"User `{user.name}` (`{user.id}`) is already banned.")

            model_cls = db.banned_user_repository.get_model_cls()
            banned_user = model_cls(
                user_id=user.id,
                reason=reason,
                from_=datetime.now(),
                until=Utils.must_parse_date_string(until) if until else None
            )
            await db.banned_user_repository.insert(banned_user)

        await self._respond_successful(interaction, f"Banned user `{user.name}` (`{user.id}`).")

    @admin.subcommand(name="unban")
    async def unban(self, interaction: Interaction[Any], user_id: str) -> None:
        """Unbans an user from using the bot.

        Parameters
        ----------
        user_id : str
            The user ID to unban.
        """
        user = await Utils.must_get_user(self._bot.client, user_id)

        with self._bot.core.enter_fazbotdb() as db:
            is_banned = await db.banned_user_repository.is_banned(user.id)
            if not is_banned:
                return await self._respond_error(interaction, f"User `{user.name}` (`{user.id}`) is not banned.")

            await db.banned_user_repository.delete(user.id)
            
        await self._respond_successful(interaction, f"Unbanned user `{user.name}` (`{user.id}`).")

    @admin.subcommand(name="echo")
    async def echo(self, interaction: Interaction[Any], message: str) -> None:
        """Echoes a message.

        Parameters
        ----------
        message : str
            The message to echo.
        """
        await interaction.send(message)

    @admin.subcommand(name="reload_asset")
    async def reload_asset(self, interaction: Interaction[Any]) -> None:
        """Reloads asset."""
        with self._bot.core.enter_asset() as asset:
            asset.read_all()

        self._bot.asset_manager.load_assets()
        await self._respond_successful(interaction, "Reloaded asset successfully.")

    @admin.subcommand(name="reload_config")
    async def reload_config(self, interaction: Interaction[Any]) -> None:
        """Reloads configs."""
        with self._bot.core.enter_config() as config:
            config.read()

        await self._respond_successful(interaction, "Reloaded config successfully.")

    @admin.subcommand(name="send")
    async def send(self, interaction: Interaction[Any], channel_id: str, message: str) -> None:
        """Unbans an user from using the bot.

        Parameters
        ----------
        channel_id : str
            The channel ID to send the message.
        message : str
            Message to send.
        """
        channel = await Utils.must_get_channel(self._bot.client, channel_id)

        if not self.__is_channel_sendable(channel):
            return await self._respond_error(interaction, f"Channel of type `{type(channel)}` does not support sending messages.") 

        try:
            await channel.send(message)  # type: ignore
        except nextcord.DiscordException as e:
            return await self._respond_error(interaction, f"Failed sending message: {e}")

        await self._respond_successful(interaction, f"Sent message on channel `{channel.name}` (`{channel.id}`).")  # type: ignore

    @admin.subcommand(name="sync_guild")
    async def sync_guild(self, interaction: Interaction[Any], guild_id: str) -> None:
        """Syncs app commands for a specific guild.

        Parameters
        ----------
        guild_id : str
            The guild ID to sync app commands to.
        """        
        guild = await Utils.must_get_guild(self._bot.client, guild_id)

        if not self.__is_whitelisted(guild.id):
            return await self._respond_error(
                interaction,
                f"Guild `{guild.name}` (`{guild.id}`) is not whitelisted. "
                f"Whitelist it first with `{self._bot.client.command_prefix}{self.whitelist.qualified_name}`"
            )

        await self._bot.client.sync_application_commands(guild_id=guild.id)
        await self._respond_successful(interaction, f"Synchronized app commands for guild `{guild.name}` (`{guild.id}`).")

    @admin.subcommand(name="sync")
    async def sync(self, interaction: Interaction[Any]) -> None:
        """Synchronizes app commands across all whitelisted guilds."""
        for guild_id in self._whitelisted_guild_ids:
            await self._bot.client.sync_application_commands(guild_id=guild_id)

        await self._respond_successful(
            interaction,
            f"Synchronized app commands across {len(self._whitelisted_guild_ids)} guilds."
        )

    @admin.subcommand(name="shutdown", description="Shuts down the bot.")
    async def shutdown(self, interaction: Interaction[Any]) -> None:
        """Shutdowns the bot enitirely."""
        await self._respond_successful(interaction, "Shutting down...")
        self._bot.stop()

    @admin.subcommand(name="whisper")
    async def whisper(self, interaction: Interaction[Any], user_id: str, message: str) -> None:
        """Whispers a message to a user.

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
            return await self._respond_error(interaction, f"Failed whispering message to user {user.display_name}: `{e}`")

        await self._respond_successful(interaction, f"Whispered message to `{user.name}` (`{user.id}`).")

    # TODO: manage syncing database and local memory
    @admin.subcommand(name="whitelist")
    async def whitelist(self, interaction: Interaction[Any], guild_id: str, option: bool = True, until: str | None = None) -> None:
        """Whitelists or unwhitelists a guild from using the bot.

        Parameters
        ----------
        guild_id : str
            The guild ID to whitelist.
        until : str | None, optional
            Date until the whitelist expires, by default None
        """
        guild = await Utils.must_get_guild(self._bot.client, guild_id)

        if self.__is_whitelisted(guild.id):
            return await self._respond_error(interaction, f"Guild `{guild.name}` (`{guild.id}`) is already whitelisted.")

        with self._bot.core.enter_fazbotdb() as db:
            model_cls = db.whitelisted_guild_repository.get_model_cls()
            whitelisted_guild = model_cls(
                guild_id=guild.id,
                guild_name=guild.name,
                from_=datetime.now(),
                until=Utils.must_parse_date_string(until) if until else None
            )
            await db.whitelisted_guild_repository.insert(whitelisted_guild)
            
        self.get_whitelisted_guild_ids().add(guild.id)
        await self._respond_successful(interaction, f"Whitelisted guild `{guild.name}` (`{guild.id}`).")

    @admin.subcommand(name="unwhitelist")
    async def unwhitelist(self, interaction: Interaction[Any], guild_id: str) -> None:
        """Unwhitelists a guild from using the bot.

        Parameters
        ----------
        guild_id : str
            The guild ID to unwhitelist.
        """
        guild = await Utils.must_get_guild(self._bot.client, guild_id)

        if not self.__is_whitelisted(guild.id):
            return await self._respond_error(interaction, f"Guild `{guild.name}` (`{guild.id}`) is not whitelisted.")

        with self._bot.core.enter_fazbotdb() as db:
            await db.whitelisted_guild_repository.delete(guild.id) 

        self.get_whitelisted_guild_ids().remove(guild.id)
        await self._respond_successful(interaction, f"Unwhitelisted guild `{guild.name}` (`{guild.id}`).")

    def __is_whitelisted(self, guild_id: int) -> bool:
        return guild_id in self.get_whitelisted_guild_ids()

    def __is_channel_sendable(self, channel: Any) -> bool:
        return hasattr(channel, "send")
