from __future__ import annotations
from abc import ABC
from io import BytesIO
from typing import TYPE_CHECKING, Any

from discord import Embed, File

from fazbot import ImageAsset

if TYPE_CHECKING:
    from discord import Interaction, InteractionMessage
    from fazbot.enum import AssetImageFile


class InvokedBase(ABC):

    _asset: ImageAsset

    def __init__(self, interaction: Interaction[Any]) -> None:
        self._interaction = interaction

    async def get_original_response(self) -> InteractionMessage:
        return await self.interaction.original_response()

    @staticmethod
    def set_embed_thumbnail_with_asset(embed: Embed, file: AssetImageFile) -> None:
        embed.set_thumbnail(url=f"attachment://{file.value}")

    @classmethod
    def get_asset_file(cls, file: AssetImageFile) -> File:
        filebytes = cls._asset.get(file)
        fileio = BytesIO(filebytes)
        return File(fileio, file.value, spoiler=False)

    @classmethod
    def set_asset(cls, asset: ImageAsset) -> None:
        cls._asset = asset

    @property
    def interaction(self) -> Interaction:
        return self._interaction


    async def _respond(self, *args: Any, **kwargs: Any) -> None:
        await self.interaction.response.send_message(*args, **kwargs)
