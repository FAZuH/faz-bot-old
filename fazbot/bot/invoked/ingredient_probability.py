from __future__ import annotations

import re
from decimal import Decimal
from typing import Any

from nextcord import Embed, Interaction

from fazbot.enum import AssetImageFile
from fazbot.util import IngredientUtil

from . import InvokedBase


class IngredientProbability(InvokedBase):

    def __init__(self, interaction: Interaction[Any], base_chance: str, loot_bonus: int, loot_quality: int) -> None:
        super().__init__(interaction)
        self._base_chance = self._parse_base_chance(base_chance)
        self._loot_bonus = loot_bonus
        self._loot_quality = loot_quality
        self._ing_util = IngredientUtil(self._base_chance, self._loot_quality, self._loot_bonus)

    async def run(self) -> None:
        embed_resp = self._get_embed(self._ing_util, self._interaction)
        await self._interaction.response.send_message(embed=embed_resp, file=self.get_asset_file(AssetImageFile.DECAYINGHEART))


    def _get_embed(self, ing_util: IngredientUtil, interaction: Interaction[Any]) -> Embed:
        one_in_n = 1 / ing_util.boosted_probability

        embed_resp = Embed(title="Ingredient Chance Calculator", color=472931)
        self.set_embed_thumbnail_with_asset(embed_resp, AssetImageFile.DECAYINGHEART)
        embed_resp.description =(
                f"Drop Chance: **{ing_util.base_probability:.2%}**\n"
                f"Loot Bonus: **{ing_util.loot_bonus}%**\n"
                f"Loot Quality: **{ing_util.loot_quality}%**\n"
                f"Loot Boost: **{ing_util.loot_boost}%**"
        )
        embed_resp.add_field(
                name="Boosted Drop Chance",
                value=f"Drop Chance: \n**{ing_util.boosted_probability:.2%}** OR **1 in {one_in_n:.2f}** mobs"
        )
        if interaction.user:
            embed_resp.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        return embed_resp

    def _parse_base_chance(self, base_chance: str) -> Decimal:
        if base_chance.endswith('%'):
            return Decimal(base_chance[:-1])
        elif '/' in base_chance:
            match = re.match(r'^(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)$', base_chance)
            if match:
                numerator = float(match.group(1))
                denominator = float(match.group(2))
                return Decimal(numerator) / Decimal(denominator)
            else:
                raise ValueError("An exception occured while trying to parse fractions: Invalid format.")
        else:
            return Decimal(base_chance)
