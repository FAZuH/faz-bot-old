from __future__ import annotations
from decimal import Decimal
import re
from typing import Any, TYPE_CHECKING

from nextcord import Embed, Interaction

from fazbot.wynn import IngredientUtil

from ..errors import *
from ._invoke import Invoke

if TYPE_CHECKING:
    from nextcord import File
    from ._asset import Asset
    from .. import Bot
    

class InvokeIngredientProbability(Invoke):

    ASSET_DECAYINGHEART: Asset

    def __init__(self, bot: Bot, interaction: Interaction[Any], base_chance: str, loot_bonus: int, loot_quality: int) -> None:
        super().__init__(bot, interaction)
        self._base_chance = self._parse_base_chance(base_chance)
        self._loot_bonus = loot_bonus
        self._loot_quality = loot_quality
        self._ing_util = IngredientUtil(self._base_chance, self._loot_quality, self._loot_bonus)

    # override
    @classmethod
    def set_assets(cls, assets: dict[str, File]) -> None:
        cls.ASSET_DECAYINGHEART = cls._get_from_assets(assets, "decayingheart.png")

    async def run(self) -> None:
        embed_resp = self._get_embed(self._ing_util, self._interaction)
        await self._interaction.send(embed=embed_resp, file=self.ASSET_DECAYINGHEART.get_file_to_send())

    def _get_embed(self, ing_util: IngredientUtil, interaction: Interaction[Any]) -> Embed:
        one_in_n = 1 / ing_util.boosted_probability

        embed_resp = Embed(title="Ingredient Chance Calculator", color=472931)
        self._set_embed_thumbnail_with_asset(embed_resp, self.ASSET_DECAYINGHEART.filename)
        embed_resp.description = (
            f"` Drop Chance  :` **{ing_util.base_probability:.2%}**\n"
            f"` Loot Bonus   :` **{ing_util.loot_bonus}%**\n"
            f"` Loot Quality :` **{ing_util.loot_quality}%**\n"
            f"` Loot Boost   :` **{ing_util.loot_boost}%**"
        )
        embed_resp.add_field(
            name="Boosted Drop Chance",
            value=f"**{ing_util.boosted_probability:.2%}** OR **1 in {one_in_n:.2f}** mobs"
        )
        if interaction.user:
            embed_resp.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)

        return embed_resp

    def _parse_base_chance(self, base_chance: str) -> Decimal:
        if base_chance.endswith('%'):
            return Decimal(base_chance[:-1]) / 100
        elif '/' in base_chance:
            match = re.match(r'^(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)$', base_chance)
            if match:
                numerator = float(match.group(1))
                denominator = float(match.group(2))
                return Decimal(numerator) / Decimal(denominator)
            else:
                raise BadArgument("Invalid format: .")
        else:
            return Decimal(base_chance)
