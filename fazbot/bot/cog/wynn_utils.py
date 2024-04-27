# pyright: reportMissingTypeStubs=false
from __future__ import annotations
from typing import TYPE_CHECKING, Any

from discord import app_commands

from . import CogBase
from fazbot.bot.invoked import ConvertEmerald, CraftedProbability, IngredientProbability

if TYPE_CHECKING:
    from discord import Interaction


class WynnUtils(CogBase):

    @app_commands.command(name="crafted_probability")
    async def _crafted_probability(
            self,
            interaction: Interaction[Any],
            ingredient1: str = CraftedProbability.INGSTR_DEFAULT,
            ingredient2: str = CraftedProbability.INGSTR_DEFAULT,
            ingredient3: str = CraftedProbability.INGSTR_DEFAULT,
            ingredient4: str = CraftedProbability.INGSTR_DEFAULT,
            ingredient5: str = CraftedProbability.INGSTR_DEFAULT,
            ingredient6: str = CraftedProbability.INGSTR_DEFAULT,
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
        await CraftedProbability(
                interaction, [ingredient1, ingredient2, ingredient3, ingredient4, ingredient5, ingredient6]
        ).run()

    @app_commands.command(name="convert_emerald")
    async def convert_emerald(self, interaction: Interaction[Any], emerald_string: str = "") -> None:
        await ConvertEmerald(interaction, emerald_string).run()

    @app_commands.command(name="ingredient_probability")
    async def ingredient_probability(self, interaction: Interaction[Any], base_chance: str, loot_bonus: int = 0, loot_quality: int = 0) -> None:
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
        await IngredientProbability(interaction, base_chance, loot_bonus, loot_quality).run()
