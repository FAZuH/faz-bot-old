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
            is_admin = ctx.author.id == self._app.config.application.admin_discord_id
        else:
            if not ctx.user:
                return False
            is_admin = ctx.user.id == self._app.config.application.admin_discord_id
        return is_admin

    def is_not_banned(self, ctx: commands.Context[Any] | Interaction[Any]) -> bool:
        if isinstance(ctx, commands.Context):
            is_not_banned = ctx.author.id not in self._app.userdata.get(UserdataFile.BANNED_USERS)
        else:
            if not ctx.user:
                return False
            is_not_banned = ctx.user.id not in self._app.userdata.get(UserdataFile.BANNED_USERS)
        return is_not_banned


