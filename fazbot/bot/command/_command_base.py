from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING, Any

from discord import Embed, File

from fazbot import ImageAsset

if TYPE_CHECKING:
    from discord import Message
    from discord.ext import commands
    from fazbot.enum import AssetImageFile


class CommandBase(ABC):

    _asset: ImageAsset

    def __init__(self, ctx: commands.Context[Any]) -> None:
        self._ctx = ctx

    @staticmethod
    def set_embed_thumbnail_with_asset(embed: Embed, file: AssetImageFile) -> None:
        embed.set_thumbnail(url=f"attachment://{file.value}")

    @classmethod
    def get_asset_file(cls, file: AssetImageFile) -> File:
        return File(cls._asset.get(file), file.value)

    @classmethod
    def set_asset(cls, asset: ImageAsset) -> None:
        cls._asset = asset

    async def _respond(self, *args: Any, **kwargs: Any) -> Message:
        return await self._ctx.send(*args, **kwargs)
