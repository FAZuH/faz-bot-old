from __future__ import annotations
from typing import Any, TYPE_CHECKING

from loguru import logger
from nextcord import Interaction

if TYPE_CHECKING:
    from . import Bot


class Checks:

    def __init__(self, bot: Bot) -> None:
        self._bot = bot
        self.load_checks()

    def load_checks(self) -> None:
        """Loads global checks to the client."""
        self.bot.client.add_application_command_check(self.is_not_banned)
        self.bot.client.add_application_command_check(self.is_whitelisted)

    async def is_admin(self, interaction: Interaction[Any]) -> bool:
        if not interaction.user:
            return False

        user_id = interaction.user.id
        is_admin = user_id == self.bot.app.properties.ADMIN_DISCORD_ID

        if not is_admin:
            logger.warning(
                f"is_admin check for user {interaction.user.global_name} ({user_id}) returned False",
                discord=True
            )

        return is_admin

    async def is_banned(self, interaction: Interaction[Any]) -> bool:
        if not interaction.user:
            return False

        user_id = interaction.user.id
        db = self.bot.fazbot_db
        is_banned = await db.whitelist_group_repository.is_banned_user(user_id)

        if is_banned:
            logger.warning(
                f"is_banned check for user {interaction.user.global_name} ({user_id}) returned True",
                discord=True
            )

        return is_banned

    async def is_whitelisted(self, interaction: Interaction[Any]) -> bool:
        if not interaction.guild:
            return False
        guild_id = interaction.guild.id

        db = self.bot.fazbot_db
        is_whitelisted = await db.whitelist_group_repository.is_whitelisted_guild(guild_id)

        if not is_whitelisted:
            logger.warning(
                f"is_whitelisted check for guild {interaction.guild.name} ({guild_id}) returned False",
                discord=True
            )

        return is_whitelisted

    async def is_not_banned(self, interaction: Interaction[Any]) -> bool:
        is_banned = await self.is_banned(interaction)
        return not is_banned

    @property
    def bot(self) -> Bot:
        return self._bot
