from __future__ import annotations
from decimal import Decimal
import re
from typing import TYPE_CHECKING

from discord import Embed

from fazbot.util import IngredientUtil

if TYPE_CHECKING:
    from discord import Interaction


class IngredientProbabilityCommand:

    def __init__(self, interaction: Interaction, base_chance: str, loot_bonus: int, loot_quality: int) -> None:
        self._interaction = interaction
        self._base_chance = self._parse_base_chance(base_chance)
        self._loot_bonus = loot_bonus
        self._loot_quality = loot_quality
        self._ing_util = IngredientUtil(base_probability=self._base_chance, loot_quality=self._loot_quality, loot_bonus=self._loot_bonus)

    async def run(self) -> None:
        one_in_n = 1 / self._ing_util.boosted_probability

        embed_resp = Embed(title="Ingredient Chance Calculator", color=472931)
        embed_resp.set_thumbnail(
            url="https://www.wynndata.tk/assets/images/items/v4//ingredients/heads/50d8ba53402f4cb0455067d068973b3d.png"
        )
        embed_resp.description =(
            f"Drop Chance: **{self._ing_util.base_probability:.2%}**\n"
            f"Loot Bonus: **{self._ing_util.loot_bonus}%**\n"
            f"Loot Quality: **{self._ing_util.loot_quality}%**"
            f"Loot Boost: **{self._ing_util.loot_boost}"
        )
        embed_resp.add_field(
            name="Boosted Drop Chance",
            value=f"Drop Chance: \n**{self._ing_util.boosted_probability:.2%}** OR **1 in {one_in_n:.2f}** mobs"
        )
        embed_resp.set_author(
            name=self._interaction.user.display_name,
            icon_url=self._interaction.user.display_avatar.url
        )

        await self._interaction.response.send_message(embed=embed_resp)


    @staticmethod
    def _parse_base_chance(base_chance: str) -> Decimal:
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
