from __future__ import annotations
from typing import TYPE_CHECKING, Any

from nextcord import Interaction

from fazbot.enum import UserdataFile

if TYPE_CHECKING:
    from fazbot import Bot


class Checks:

    def __init__(self, bot: Bot) -> None:
        self._bot = bot

    def is_admin(self, interaction: Interaction[Any]) -> bool:
        if not interaction.user:
            return False

        user_id = interaction.user.id
        is_admin = user_id == self._bot.core.config.application.admin_discord_id
        self._bot.core.logger.console_logger.debug(f"check {self.is_admin.__name__}: {user_id} is {is_admin}.")

        return is_admin

    def is_not_banned(self, interaction: Interaction[Any]) -> bool:
        if not interaction.user:
            return False

        user_id = interaction.user.id
        is_not_banned = user_id not in self._bot.core.userdata.get(UserdataFile.BANNED_USERS)
        return is_not_banned

    def load_checks(self) -> None:
        self._bot.client.add_application_command_check(self.is_not_banned)
