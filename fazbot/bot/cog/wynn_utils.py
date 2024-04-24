# pyright: reportMissingTypeStubs=false
from __future__ import annotations
from typing import TYPE_CHECKING, Any

from discord.ext import commands

from fazbot.bot.command import ConvertEmeraldCommand, CraftedProbabilityCommand, IngredientProbabilityCommand

from . import CogBase

if TYPE_CHECKING:
    from discord.ext.commands import Context


class WynnUtils(CogBase):

    @commands.hybrid_command(name="crafted_probability")
    async def _crafted_probability(
            self,
            ctx: Context[Any],
            ingredient1: str = "0,0,0",
            ingredient2: str = "0,0,0",
            ingredient3: str = "0,0,0",
            ingredient4: str = "0,0,0",
            ingredient5: str = "0,0,0",
            ingredient6: str = "0,0,0",
    ) -> None:
        """Calculates crafted roll probabilities.
        improved with help from afterfive.

        Parameters
        -----------
        ingredient1: str
            min,max[,efficiency]
        ingredient2: str
            min,max[,efficiency]
        ingredient3: str
            min,max[,efficiency]
        ingredient5: str
            min,max[,efficiency]
        ingredient6: str
            min,max[,efficiency]
        ingredient4: str
            min,max[,efficiency]
        """
        await CraftedProbabilityCommand(
                ctx, [ingredient1, ingredient2, ingredient3, ingredient4, ingredient5, ingredient6]
        ).run()

    @commands.hybrid_command(name="convert_emerald")
    async def _convert_emerald(self, ctx: Context[Any], emerald_string: str = "") -> None:
        await ConvertEmeraldCommand(ctx, emerald_string).run()

    @commands.hybrid_command(name="ingredient_probability")
    async def _ingredient_probability(self, ctx: Context[Any], base_chance: str, loot_bonus: int, loot_quality: int) -> None:
        """Calculates ingredient drop probability after loot bonus and loot quality.

        Parameters
        -----------
        base_chance: str
            Ingredient base drop chance. (Supported format: 1.2%, 1.2/100, 0.012)
        loot_bonus: int
            Loot bonus value.
        loot_quality: int
            Loot quality value.
        """
        await IngredientProbabilityCommand(ctx, base_chance, loot_bonus, loot_quality).run()
