from typing import Any

import nextcord
from nextcord import Interaction

from .. import Utils
from . import CogBase


class Admin(CogBase):

    # @override
    def cog_application_command_check(self, interaction: Interaction[Any]) -> bool:
        return self._bot.checks.is_admin(interaction)

    @nextcord.slash_command(name="admin", description="Admin commands.")
    async def admin(self, interaction: Interaction[Any]) -> None:
        ...

    @admin.subcommand(name="ban", description="Bans an user from using the bot.")
    async def ban(self, interaction: Interaction[Any], user_id: str) -> None:
        user = await Utils.must_get_user(self._bot.client, user_id)
        banned_users = self._bot.core.userdata.get(self._bot.core.userdata.enum.BANNED_USERS)

        if user.id in banned_users:
            await interaction.send(f"User `{user.name}` (`{user.id}`) is already banned.")
            return

        # TODO: not thread safe
        banned_users.append(user.id)  # type: ignore
        self._bot.core.userdata.save(self._bot.core.userdata.enum.BANNED_USERS)

        await interaction.send(f"Banned user `{user.name}` (`{user.id}`).")

    @admin.subcommand(name="unban", description="Unbans an user from using the bot.")
    async def unban(self, interaction: Interaction[Any], user_id: str) -> None:
        user = await Utils.must_get_user(self._bot.client, user_id)

        banned_users = self._bot.core.userdata.get(self._bot.core.userdata.enum.BANNED_USERS)

        if user.id not in banned_users:
            await interaction.send(f"User `{user.name}` (`{user.id}`) is not banned.")
            return

        banned_users.remove(user.id)  # type: ignore
        self._bot.core.userdata.save(self._bot.core.userdata.enum.BANNED_USERS)

        await interaction.send(f"Unbanned user `{user.name}` (`{user.id}`).")

    @admin.subcommand(name="echo", description="Echoes a message.")
    async def echo(self, interaction: Interaction[Any], message: str) -> None:
        await interaction.send(message)

    @admin.subcommand(name="reload_asset", description="Reloads asset.")
    async def reload_asset(self, interaction: Interaction[Any]) -> None:
        self._bot.core.get_asset_threadsafe()().load()
        await interaction.send("Reloaded asset successfully.")

    @admin.subcommand(name="reload_config", description="Reloads configs.")
    async def reload_config(self, interaction: Interaction[Any]) -> None:
        self._bot.core.get_config_threadsafe().load()
        await interaction.send("Reloaded config successfully.")

    @admin.subcommand(name="reload_userdata", description="Reloads userdata.")
    async def reload_userdata(self, interaction: Interaction[Any]) -> None:
        self._bot.core.userdata.load()
        await interaction.send("Reloaded userdata successfully.")

    @admin.subcommand(name="send", description="Sends a message to a channel.")
    async def send(self, interaction: Interaction[Any], channel_id: str, message: str) -> None:
        channel = await Utils.must_get_channel(self._bot.client, channel_id)

        if not hasattr(channel, "send"):
            await interaction.send(f"Channel of type `{type(channel)}` does not support sending messages.")
            return

        try:
            await channel.send(message)  # type: ignore
        except nextcord.DiscordException as e:
            await interaction.send(f"Failed to send message: {e}")

        await interaction.send(f"Sent message on channel `{channel.name}` (`{channel.id}`).")  # type: ignore

    @admin.subcommand(name="sync_guild", description="Synchronizes app commands for a specific guild.")
    async def sync_guild(self, interaction: Interaction[Any], guild_id: str) -> None:
        guild = await Utils.must_get_guild(self._bot.client, guild_id)

        if guild.id not in self._bot.core.userdata.get(self._bot.core.userdata.enum.WHITELISTED_GUILDS):
            await interaction.send(
                    f"Guild `{guild.name}` (`{guild.id}`) is not whitelisted. "
                    f"Whitelist it first with `{self._bot.client.command_prefix}{self.whitelist.qualified_name}`"
            )
            return

        await self._bot.client.sync_application_commands(guild_id=guild.id)

        await interaction.send(f"Synchronized app commands for guild `{guild.name}` (`{guild.id}`).")

    @admin.subcommand(name="sync", description="Synchronizes app commands across all whitelisted guilds.")
    async def sync(self, interaction: Interaction[Any]) -> None:
        guilds_len = 0

        for guild_id in self._bot.core.userdata.get(self._bot.core.userdata.enum.WHITELISTED_GUILDS):
            assert isinstance(guild_id, int)
            await self._bot.client.sync_application_commands(guild_id=guild_id)
            guilds_len += 1

        await interaction.send(f"Synchronized app commands across {guilds_len} guilds.")

    @admin.subcommand(name="shutdown", description="Shuts down the bot.")
    async def shutdown(self, interaction: Interaction[Any]) -> None:
        await interaction.send("Shutting down...")
        self._bot.stop()

    @admin.subcommand(name="whisper", description="Whispers a message to a user.")
    async def whisper(self, interaction: Interaction[Any], user_id: str, message: str) -> None:
        user = await Utils.must_get_user(self._bot.client, user_id)

        try:
            await user.send(message)
        except nextcord.DiscordException as e:
            await interaction.send(f"Failed whispering message to user {user.display_name}: `{e}`")

        await interaction.send(f"Whispered message to `{user.name}` (`{user.id}`).")

    @admin.subcommand(name="whitelist", description="Whitelists a guild.")
    async def whitelist(self, interaction: Interaction[Any], guild_id: str, option: bool = True) -> None:
        guild = await Utils.must_get_guild(self._bot.client, guild_id)

        whitelisted_guilds: list[int] = self._bot.core.userdata.get(self._bot.core.userdata.enum.WHITELISTED_GUILDS)  # type: ignore
        if option:
            if guild.id in whitelisted_guilds:
                whitelisted_guilds.append(guild.id)
                await interaction.send(f"Whitelisted guild `{guild.name}` (`{guild.id}`).")
            else:
                await interaction.send(f"Guild `{guild.name}` (`{guild.id}`) is already whitelisted.")
        else:
            if guild.id in whitelisted_guilds:
                whitelisted_guilds.remove(guild.id)
                await interaction.send(f"Unwhitelisted guild `{guild.name}` (`{guild.id}`).")
            else:
                await interaction.send(f"Guild `{guild.name}` (`{guild.id}`) is not whitelisted.")

        self._bot.core.userdata.save(self._bot.core.userdata.enum.WHITELISTED_GUILDS)
