from __future__ import annotations

from abc import ABC, abstractmethod
from io import BytesIO
from typing import TYPE_CHECKING, Any

from nextcord import Embed, File, Interaction

from fazbot import ImageAsset

if TYPE_CHECKING:
    from nextcord import InteractionMessage

    from fazbot.enum import AssetImageFile


class Invoke(ABC):

    def __init__(self, interaction: Interaction[Any]) -> None:
        self._interaction = interaction

    @staticmethod
    def set_embed_thumbnail_with_asset(embed: Embed, file: AssetImageFile) -> None:
        embed.set_thumbnail(url=f"attachment://{file.value}")

    @abstractmethod
    @classmethod
    def load_asset(cls, assets: dict[str, BytesIO]) -> None: ...

