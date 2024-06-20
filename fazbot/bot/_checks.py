from __future__ import annotations
from typing import Any, TYPE_CHECKING

from nextcord import Interaction

if TYPE_CHECKING:
    from fazbot import Bot


class Checks:

    def __init__(self, bot: Bot) -> None:
        self._bot = bot

    def is_admin(self, interaction: Interaction[Any]) -> bool:
        if not interaction.user:
            return False

        user_id = interaction.user.id
        with self._bot.core.enter_config() as config:
            is_admin = user_id == config.admin_discord_id

        with self._bot.core.enter_logger() as logger:
            logger.console.debug(f"check {self.is_admin.__name__}: {user_id} is {is_admin}.")

        return is_admin

    async def is_not_banned(self, interaction: Interaction[Any]) -> bool:
        if not interaction.user:
            return False

        with self._bot.core.enter_fazbotdb() as db:
            is_not_banned = await db.banned_user_repository.is_banned(interaction.user.id)

        return is_not_banned

    def load_checks(self) -> None:
        """Loads global checks to the client."""
        self._bot.client.add_application_command_check(self.is_not_banned)
