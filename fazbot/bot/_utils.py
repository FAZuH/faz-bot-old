from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Callable, TypeVar

from dateparser import parse

P = TypeVar('P')

if TYPE_CHECKING:
    from nextcord import Guild, Interaction, PartialMessageable, Thread, User
    from nextcord.abc import GuildChannel, PrivateChannel
    from nextcord.ext.commands import Bot, Context


class Utils:

    @staticmethod
    async def parse_big_int(interaction: Interaction[Any], value: str) -> int | None:
        try:
            return int(value)
        except ValueError:
            await interaction.response.send_message(f"Failed parsing {value} into an integer.")

    @staticmethod
    async def parse_date(interaction: Interaction[Any], value: str) -> datetime | None:
        try:
            return parse(value)
        except ValueError:
            await interaction.response.send_message(f"Failed parsing {value} into a date.")

    @staticmethod
    async def must_get_channel(bot: Bot, interaction: Interaction[Any], channel_id: str) -> GuildChannel | Thread | PrivateChannel | PartialMessageable | None:
        return await Utils.must_getter(bot.get_channel, interaction, channel_id, "channel")

    @staticmethod
    async def must_get_guild(bot: Bot, interaction: Interaction[Any], guild_id: str) -> Guild | None:
        return await Utils.must_getter(bot.get_guild, interaction, guild_id, "guild")

    @staticmethod
    async def must_get_user(bot: Bot, interaction: Interaction[Any], user_id: str) -> User | None:
        return await Utils.must_getter(bot.get_user, interaction, user_id, "user")

    @staticmethod
    async def must_getter(getter_func: Callable[[int], P | None], interaction: Interaction[Any], id_: str, type: str) -> P | None:
        try:
            id__ = int(id_)
        except ValueError:
            await interaction.send(f"Failed parsing {id_} into an integer.")
            return
        if not id__:
            return
        if not (user := getter_func(id__)):
            await interaction.send(f"{type.title()} with ID `{id__}` not found.")
            return
        return user
