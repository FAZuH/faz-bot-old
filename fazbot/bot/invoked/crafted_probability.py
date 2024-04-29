# pyright: reportUnknownMemberType=false, reportUnknownArgumentType=false, reportUnknownVariableType=false, reportMissingTypeStubs=false
from __future__ import annotations

from decimal import Decimal
from io import BytesIO
from typing import Any, Callable

import matplotlib.pyplot as plt
from nextcord import ButtonStyle, Colour, Embed, File, Interaction, errors, ui

from fazbot.enum import AssetImageFile
from fazbot.object import WynnIngredientValue
from fazbot.util import CacheUtil, CraftedUtil

from . import InvokedBase


class CraftedProbability(InvokedBase):

    INGSTR_DEFAULT = "0,0,0"

    def __init__(self, interaction: Interaction[Any], ing_strs: list[str]) -> None:
        super().__init__(interaction)
        self._ing_strs = ing_strs

        self._cache = CacheUtil()
        self._cache.register(self, [self._get_craftprobs_embed, self._get_atleast_embed, self._get_atmost_embed, self._get_plot_embed, self._get_plot_file])

        self._assetfile = self.get_asset_file(AssetImageFile.CRAFTINGTABLE)
        self._craftutil = CraftedUtil(self._parse_ings_str(ing_strs))
        self._craftutil.run()
        self._view = self._View(self)

    async def run(self) -> None:
        embed = self._get_craftprobs_embed(self.interaction, self._craftutil)
        try:
            await self.interaction.send(embed=embed, view=self._view, file=self._assetfile)
        except errors.HTTPException as e:
            # fallback to sending plot if embed size exceeds maximum size
            if e.code == 50035:
                embed = self._get_plot_embed(self._craftutil.craft_probs)
                dist_plot = self._get_plot_file(self._craftutil.craft_probs)
                await self.interaction.send(embed=embed, file=dist_plot)
            else:
                raise e

    def _parse_ings_str(self, ing_strs: list[str]) -> list[WynnIngredientValue]:
        res: list[WynnIngredientValue] = []
        for ing_str in ing_strs:
            if ing_str == CraftedProbability.INGSTR_DEFAULT:
                continue
            ing_str = ing_str.strip()
            ing_vals = ing_str.split(",")
            if len(ing_vals) not in {1, 3}:
                raise ValueError("Invalid ingredient format. Must be in format of 'min,max[,efficiency]'")
            parsed_ing_vals: list[int] = []
            for val in ing_vals:
                try:
                    parsed_ing_vals.append(int(val))
                except ValueError:
                    raise ValueError(f"Exception occured while parsing ingredient value {val}")
            res.append(WynnIngredientValue(*parsed_ing_vals))

        return res

    def _get_base_embed(self, interaction: Interaction[Any], craftutil: CraftedUtil) -> Embed:
        embed = Embed(title="Crafteds Probabilites Calculator", color=8894804)
        self.set_embed_thumbnail_with_asset(embed, AssetImageFile.CRAFTINGTABLE)
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

    def _get_plot_embed(self, craftprobs: dict[int, Decimal]) -> Embed:
        embed = Embed(title="Error", color=Colour.red())

        min_roll = min(craftprobs)
        min_prob = craftprobs[min_roll]
        one_in_n_min = round(Decimal(1 / craftprobs[min_roll]), 2)

        max_roll = max(craftprobs)
        max_prob = craftprobs[max_roll]
        one_in_n_max = round(Decimal(1 / craftprobs[max_roll]), 2)

        embed.description = (
                f"**Embed size exceeds maximum size of 6000 characters. Attaching plot instead.**\n"
                f"- Min Roll: **{min_roll}**, Probability: **{min_prob * 100:.2f}%** (1 in {one_in_n_min:,})\n"
                f"- Max Roll: **{max_roll}**, Probability: **{max_prob * 100:.2f}%** (1 in {one_in_n_max:,})"
        )
        return embed

    def _get_plot_file(self, craftprobs: dict[int, Decimal]) -> File:
        if len(craftprobs) > 200:
            plt.plot(list(craftprobs.keys()), list(craftprobs.values()), marker='o')  # type: ignore
        else:
            keys_list = list(craftprobs)
            diffs = [keys_list[index + 1] - roll for index, roll in enumerate(keys_list[:-1])]
            bar_width = min(diffs) * 0.9
            plt.bar(list(craftprobs.keys()), list(craftprobs.values()), width=bar_width)  # type: ignore

        plt.title('Roll Probability Distribution')
        plt.ylabel('Probability')
        plt.xlabel('Roll')
        plt.gca().set_axisbelow(True)
        plt.grid(visible=True, alpha=.3)

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        return File(buffer, filename="graph.png")

    class _View(ui.View):
        def __init__(self, cmd: CraftedProbability):
            super().__init__(timeout=60)
            self._cmd = cmd
            self._interaction = cmd.interaction
            self._craftutil = cmd._craftutil

        # @override
        async def on_timeout(self) -> None:
            # Disable all items on timeout
            for item in self.children:
                self.remove_item(item)
            await self._cmd.interaction.edit_original_message(view=self)

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
                embedfactory: Callable[[Interaction[Any], CraftedUtil], Embed] | None = None,
            ) -> None:
            await interaction.response.defer()
            self._click_button(button)
            embed = embedfactory(interaction, self._craftutil) if embedfactory else None
            await interaction.edit_original_message(embed=embed, view=self)

        def _click_button(self, button: ui.Button[CraftedProbability._View]) -> None:
            for item in self.children:
                if isinstance(item, ui.Button):
                    item.disabled = False
            button.disabled = True
