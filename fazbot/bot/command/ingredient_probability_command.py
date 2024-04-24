# pyright: reportMissingTypeStubs=false
from __future__ import annotations
from decimal import Decimal
import re
from typing import TYPE_CHECKING, Any

from discord import Embed

from . import CommandBase
from fazbot.util import IngredientUtil

if TYPE_CHECKING:
    from discord.ext.commands import Context


class IngredientProbabilityCommand(CommandBase):

    def __init__(self, ctx: Context[Any], base_chance: str, loot_bonus: int, loot_quality: int) -> None:
        super().__init__(ctx)
        self._base_chance = self._parse_base_chance(base_chance)
        self._loot_bonus = loot_bonus
        self._loot_quality = loot_quality
        self._ing_util = IngredientUtil(self._base_chance, self._loot_quality, self._loot_bonus)

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
                name=self._ctx.author.display_name,
                icon_url=self._ctx.author.display_avatar.url
        )

        await self._ctx.send(embed=embed_resp)


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
