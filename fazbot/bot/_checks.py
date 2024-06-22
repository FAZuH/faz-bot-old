from __future__ import annotations
from typing import Any, TYPE_CHECKING

from nextcord import Interaction

if TYPE_CHECKING:
    from fazbot import Bot


class Checks:

    def __init__(self, bot: Bot) -> None:
        self._bot = bot

    async def is_admin(self, interaction: Interaction[Any]) -> bool:
        if not interaction.user:
            return False

        user_id = interaction.user.id
        is_admin = user_id == self._bot.core.config.admin_discord_id

        if not is_admin:
            await self._bot.logger.discord.warning(f"is_admin check for user {interaction.user.global_name} ({user_id}) retruned False")

        return is_admin

    async def is_banned(self, interaction: Interaction[Any]) -> bool:
        if not interaction.user:
            return False

        user_id = interaction.user.id
        with self._bot.core.enter_fazbotdb() as db:
            is_banned = await db.banned_user_repository.is_exists(user_id)

        if is_banned:
            await self._bot.logger.discord.warning(f"is_banned check for user {interaction.user.global_name} ({user_id}) returned True")

        return is_banned

    async def is_whitelisted(self, interaction: Interaction[Any]) -> bool:
        if not interaction.guild:
            return False

        guild_id = interaction.guild.id
        with self._bot.core.enter_fazbotdb() as db:
            is_whitelisted = await db.whitelisted_guild_repository.is_exists(guild_id)

        if not is_whitelisted:
            await self._bot.logger.discord.warning(f"is_whitelisted check for user {interaction.guild.name} ({guild_id}) returned False")

        return is_whitelisted

    async def is_not_banned(self, interaction: Interaction[Any]) -> bool:
        is_banned = await self.is_banned(interaction)
        return not is_banned

    def load_checks(self) -> None:
        """Loads global checks to the client."""
        self._bot.client.add_application_command_check(self.is_not_banned)
        self._bot.client.add_application_command_check(self.is_whitelisted)
