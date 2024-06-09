from __future__ import annotations

from io import BytesIO
from typing import Any, TYPE_CHECKING

from nextcord import Embed, File, Interaction

from fazbot import ImageAsset

if TYPE_CHECKING:
    from nextcord import InteractionMessage
    from fazbot.enum import AssetImageFile


class InvokedBase:

    _asset: ImageAsset

    def __init__(self, interaction: Interaction[Any]) -> None:
        self._interaction = interaction

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
    def interaction(self) -> Interaction[Any]:
        return self._interaction
