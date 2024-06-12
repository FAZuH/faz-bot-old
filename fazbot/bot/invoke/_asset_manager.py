from io import BytesIO
from pathlib import Path

from nextcord import File

from . import InvokeConvertEmerald, InvokeCraftedProbability, InvokeIngredientProbability


class AssetManager:
    """Class for managing assets for Invoke classes.
    Assets passed or set into the `asset` property
    is automatically converted into a dictionary of
    `dict[str, File]`. The converted asset is then 
    passed into class variables of Invoke subclasses
    automatically."""

    def __init__(self, assets: dict[Path, bytes]) -> None:
        self.assets = assets

    def set_invoke_assets(self) -> None:
        InvokeConvertEmerald.set_assets(self.assets)
        InvokeCraftedProbability.set_assets(self.assets)
        InvokeIngredientProbability.set_assets(self.assets)

    def _convert_asset_file_type(self, assets: dict[Path, bytes]) -> dict[str, File]:
        assets_: dict[str, File] = {}
        for fp, asset in assets.items():
            fileio = BytesIO(asset)
            file = File(fileio)
            assets_[fp.stem] = file
        return assets_

    @property
    def assets(self) -> dict[str, File]:
        return self._assets
        
    @assets.setter
    def assets(self, assets: dict[Path, bytes]) -> None:
        self._assets = self._convert_asset_file_type(assets)
        self.set_invoke_assets()

