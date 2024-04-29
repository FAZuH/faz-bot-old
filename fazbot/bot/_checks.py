from __future__ import annotations

from typing import TYPE_CHECKING, Any

from nextcord import Interaction
from nextcord.ext import commands

from fazbot.enum import UserdataFile

if TYPE_CHECKING:
    from fazbot import Core


class Checks:

    def __init__(self, app: Core) -> None:
        self._app = app

    def is_admin(self, ctx: commands.Context[Any] | Interaction[Any]) -> bool:
        if isinstance(ctx, commands.Context):
            user_id = ctx.author.id
        else:
            if not ctx.user:
                return False
            user_id = ctx.user.id
        is_admin = user_id == self._app.config.application.admin_discord_id
        self._app.logger.console_logger.debug(f"check {self.is_admin.__name__}: {user_id} is {is_admin}.")
        return is_admin

    def is_not_banned(self, ctx: commands.Context[Any] | Interaction[Any]) -> bool:
        if isinstance(ctx, commands.Context):
            user_id = ctx.author.id
        else:
            if not ctx.user:
                return False
            user_id = ctx.user.id
        is_not_banned = user_id not in self._app.userdata.get(UserdataFile.BANNED_USERS)
        return is_not_banned


