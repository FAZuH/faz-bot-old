from __future__ import annotations
from decimal import Decimal
from typing import Any, Callable, TYPE_CHECKING

from nextcord import ButtonStyle, Embed, Interaction, ui

from fazbot.util import CacheUtil
from fazbot.wynn import CraftedUtil, IngredientField

from ..errors import *
from ._invoke import Invoke

if TYPE_CHECKING:
    from nextcord import File
    from ._asset import Asset
    from .. import Bot


class InvokeCraftedProbability(Invoke):

    ASSET_CRAFTINGTABLE: Asset
    INGSTR_DEFAULT = "0,0,0"

    def __init__(self, bot: Bot, interaction: Interaction[Any], ing_strs: list[str]) -> None:
        super().__init__(bot, interaction)
        self._ing_strs = ing_strs

        self._cache = CacheUtil()
        self._cache.register(self, [self._get_craftprobs_embed, self._get_atleast_embed, self._get_atmost_embed])

        self._craftutil = CraftedUtil(self._parse_ings_str(ing_strs))
        self._view = self._View(self)

    # override
    @classmethod
    def set_assets(cls, assets: dict[str, File]) -> None:
        cls.ASSET_CRAFTINGTABLE = cls._get_from_assets(assets, "craftingtable.png")

    async def run(self) -> None:
        embed = self._get_craftprobs_embed(self._interaction, self._craftutil)
        await self._interaction.send(embed=embed, view=self._view, file=self.ASSET_CRAFTINGTABLE.get_file_to_send())

    def _parse_ings_str(self, ing_strs: list[str]) -> list[IngredientField]:
        res: list[IngredientField] = []
        for ing_str in ing_strs:
            if ing_str == InvokeCraftedProbability.INGSTR_DEFAULT:
                continue
            ing_str = ing_str.strip()
            ing_vals = ing_str.split(",")
            if len(ing_vals) not in {2, 3}:
                raise BadArgument(f"Invalid format on {ing_str}. Value must be 'min,max[,efficiency]'")
            try:
                parsed_ing_vals: list[int] = [int(v) for v in ing_vals]
            except ValueError:
                raise BadArgument(f"Failed parsing ingredient value on {ing_str}")
            try:
                res.append(IngredientField(*parsed_ing_vals))
            except ValueError as e:
                raise BadArgument(e.args[0]) from e
        return res

    def _get_base_embed(self, interaction: Interaction[Any], craftutil: CraftedUtil) -> Embed:
        embed = Embed(title="Crafteds Probabilites Calculator", color=8894804)
        self._set_embed_thumbnail_with_asset(embed, self.ASSET_CRAFTINGTABLE.filename)
        if interaction.user:
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        # Embed descriptions
        embed_desc = [f"Ingredients:"]
        for i, ing in enumerate(craftutil.ingredients, start=1):
            ing_info = f"- `[{i}]`: {ing.min_value} to {ing.max_value}"  # -[nth]: min to max
            ing_info += f", {ing.boost}% boost" if ing.boost != 0 else ""  # Add boost to info if exist
            embed_desc.append(ing_info)
        embed.description = "\n".join(embed_desc)
        return embed

    def _get_craftprobs_embed(self, interaction: Interaction[Any], craftutil: CraftedUtil) -> Embed:
        embed = self._get_base_embed(interaction, craftutil)
        embed_fields_values = ""
        is_first_embed = True
        for value, probability in craftutil.craft_probs.items():
            one_in_n = round(Decimal(1 / probability), 2)
            result = f"Roll: **{value}**, Chance: **{probability * 100:.2f}%** (1 in {one_in_n:,})"
            if len(embed_fields_values + f"{result}\n") > 1024:
                embed.add_field(name="Probabilities" if is_first_embed else "", value=embed_fields_values, inline=False)
                embed_fields_values = ""
                is_first_embed = False
            embed_fields_values += f"{result}\n"
        embed.add_field(name="Probabilities" if is_first_embed else "", value=embed_fields_values, inline=False)
        return embed

    def _get_atleast_embed(self, interaction: Interaction[Any], craftutil: CraftedUtil) -> Embed:
        embed = self._get_base_embed(interaction, craftutil)
        field_value = ""
        cmlr_prob = 1
        is_first_embed = True
        for val, prob in craftutil.craft_probs.items():
            one_in_n = round(Decimal(1 / cmlr_prob), 2)
            line = f"Roll: **atleast {val}**, Chance: **{cmlr_prob * 100:.2f}%** (1 in {one_in_n:,})"
            if len(field_value + f"{line}\n") > 1024:
                embed.add_field(name="Probabilities" if is_first_embed else "", value=field_value, inline=False)
                field_value = ""
                is_first_embed = False
            cmlr_prob -= prob
            field_value += f"{line}\n"
        embed.add_field(name="Probabilities" if is_first_embed else "", value=field_value, inline=False)
        return embed

    def _get_atmost_embed(self, interaction: Interaction[Any], craftutil: CraftedUtil) -> Embed:
        embed = self._get_base_embed(interaction, craftutil)
        field_value = ""
        cml_prob = 0
        is_first_embed = True
        for val, prob in craftutil.craft_probs.items():
            cml_prob += prob
            one_in_n = round(Decimal(1 / cml_prob), 2)
            line = f"Roll: **atmost {val}**, Chance: **{cml_prob * 100:.2f}%** (1 in {one_in_n:,})"
            if len(field_value + f"{line}\n") > 1024:
                embed.add_field(name="Probabilities" if is_first_embed else "", value=field_value, inline=False)
                field_value = ""
                is_first_embed = False
            field_value += f"{line}\n"
        embed.add_field(name="Probabilities" if is_first_embed else "", value=field_value, inline=False)
        return embed

    class _View(ui.View):
        def __init__(self, cmd: InvokeCraftedProbability):
            super().__init__(timeout=60)
            self._cmd = cmd
            self._interaction = cmd._interaction
            self._craftutil = cmd._craftutil

        # override
        async def on_timeout(self) -> None:
            # Disable all items on timeout
            for item in self.children:
                self.remove_item(item)
            await self._cmd._interaction.edit_original_message(view=self)

        @ui.button(label="Distribution", style=ButtonStyle.green, emoji="🎲", disabled=True)
        async def button_distribution(self, button: ui.Button[Any], interaction: Interaction[Any]) -> None:
            await self._do_button(button, interaction, self._cmd._get_craftprobs_embed)

        @ui.button(label="Atleast", style=ButtonStyle.green, emoji="📉")
        async def button_atleast(self, button: ui.Button[Any], interaction: Interaction[Any]) -> None:
            await self._do_button(button, interaction, self._cmd._get_atleast_embed)

        @ui.button(label="Atmost", style=ButtonStyle.green, emoji="📈")
        async def button_atmost_callback(self, button: ui.Button[Any], interaction: Interaction[Any]) -> None:
            await self._do_button(button, interaction, self._cmd._get_atmost_embed)

        async def _do_button(
                self,
                button: ui.Button[Any],
                interaction: Interaction[Any],
                embed_strategy: Callable[[Interaction[Any], CraftedUtil], Embed] | None = None,
            ) -> None:
            await interaction.response.defer()
            self._click_button(button)
            embed = embed_strategy(interaction, self._craftutil) if embed_strategy else None
            await interaction.edit_original_message(embed=embed, view=self)

        def _click_button(self, button: ui.Button[InvokeCraftedProbability._View]) -> None:
            for item in self.children:
                if isinstance(item, ui.Button):
                    item.disabled = False
            button.disabled = True
