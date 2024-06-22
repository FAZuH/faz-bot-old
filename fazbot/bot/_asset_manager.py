from __future__ import annotations
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING

from nextcord import File

from .invoke import InvokeConvertEmerald, InvokeCraftedProbability, InvokeIngredientProbability

if TYPE_CHECKING:
    from fazbot import Bot


class AssetManager:
    """Class for managing assets for Invoke classes. Assets passed or set into the `asset` property
    is automatically converted into a dictionary of `dict[str, File]`. The converted asset is then 
    passed into class variables of Invoke subclasses automatically."""

    def __init__(self, bot: Bot) -> None:
        self._bot = bot
    
    def load_assets(self) -> None:
        asset = self._bot.core.asset
        self._assets = self.__convert_asset_file_type(asset.files)
        self.__set_invoke_assets()

    def __set_invoke_assets(self) -> None:
        InvokeConvertEmerald.set_assets(self._assets)
        InvokeCraftedProbability.set_assets(self._assets)
        InvokeIngredientProbability.set_assets(self._assets)

    def __convert_asset_file_type(self, assets: dict[Path, bytes]) -> dict[str, File]:
        assets_: dict[str, File] = {}
        for fp, asset in assets.items():
            fileio = BytesIO(asset)
            file = File(fileio, filename=fp.name)
            assets_[fp.name] = file
        return assets_
