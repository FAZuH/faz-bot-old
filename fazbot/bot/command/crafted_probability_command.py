# pyright: reportUnknownMemberType=false, reportUnknownArgumentType=false, reportUnknownVariableType=false
from __future__ import annotations
from decimal import Decimal
from io import BytesIO
from typing import TYPE_CHECKING, Any

from discord import ButtonStyle, Colour, Embed, InteractionMessage, errors, File
from discord.ui import button, Button, View
import matplotlib.pyplot as plt

from . import CommandBase
from fazbot.object import WynnIngredientValue
from fazbot.util import CraftedUtil

if TYPE_CHECKING:
    from discord import Interaction


class CraftedProbabilityCommand(CommandBase):

    def __init__(self, interaction: Interaction, ing_strs: list[str]) -> None:
        self._interaction = interaction
        self._ing_strs = ing_strs
        self._crafted_util = CraftedUtil(self._parse_ings_str(ing_strs))

    async def run(self):
        embed_resp = self._get_embed(self._interaction, self._crafted_util)
        try:
            view = self._View(self)
            await self._respond(embed=embed_resp, view=view)
        except errors.HTTPException as e:
            if e.code == 50035:
                embed_resp = Embed(title="Error", color=Colour.red())

                min_roll = min(self._crafted_util.craft_probs)
                min_prob = self._crafted_util.craft_probs[min_roll]
                one_in_n_min = round(Decimal(1 / self._crafted_util.craft_probs[min_roll]), 2)

                max_roll = max(self._crafted_util.craft_probs)
                max_prob = self._crafted_util.craft_probs[max_roll]
                one_in_n_max = round(Decimal(1 / self._crafted_util.craft_probs[max_roll]), 2)

                embed_resp.description = (
                        f"**Embed size exceeds maximum size of 6000. Attaching plot instead.**\n"
                        f"- Min Roll: **{min_roll}**, Probability: **{min_prob * 100:.2f}%** (1 in {one_in_n_min:,})\n"
                        f"- Max Roll: **{max_roll}**, Probability: **{max_prob * 100:.2f}%** (1 in {one_in_n_max:,})"
                )

                await self._interaction.response.send_message(embed=embed_resp, file=self._get_plot(self._crafted_util.craft_probs))
            else:
                raise e

    def _get_embed(self, interaction: Interaction, crafted_util: CraftedUtil) -> Embed:
        embed_resp = Embed(title="Crafteds Probabilites Calculator", color=8894804)
        embed_resp.set_thumbnail(url="https://i.ibb.co/jTQtJGb/favpng-square-text-pattern.png")
        embed_resp.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url
        )

        # Embed descriptions
        embed_desc = [f"Ingredients:"]
        for i, ing in enumerate(crafted_util.ingredients, start=1):
            ing_info = f"- `[{i}]`: {ing.min_value} to {ing.max_value}"  # -[nth]: min to max
            ing_info += f", {ing.boost}% boost" if ing.boost != 0 else ""  # Add boost to info if exist
            embed_desc.append(ing_info)
        embed_resp.description = "\n".join(embed_desc)

        # Embed fields
        self._modify_embed_craftprobs(crafted_util.craft_probs, embed_resp)
        return embed_resp

    def _parse_ings_str(self, ing_strs: list[str]) -> list[WynnIngredientValue]:
        res: list[WynnIngredientValue] = []
        for ing_str in ing_strs:
            ing_str = ing_str.strip()
            ing_vals = ing_str.split(",")
            if len(ing_vals) not in {1, 3}:
                raise ValueError("Invalid ingredient format. Must be in format of 'min,max[,boost]'")
            parsed_ing_vals: list[int] = []
            for val in ing_vals:
                try:
                    parsed_ing_vals.append(int(val))
                except ValueError:
                    raise ValueError(f"Exception occured while parsing ingredient value {val}")
            res.append(WynnIngredientValue(*parsed_ing_vals))
        return res

    def _modify_embed_craftprobs(self, craft_probs: dict[int, Decimal], embed: Embed) -> None:
        embed_fields_values = ""
        is_first_embed = True
        for value, probability in craft_probs.items():
            one_in_n = round(Decimal(1 / probability), 2)
            result = f"Roll: **{value}**, Chance: **{probability * 100:.2f}%** (1 in {one_in_n:,})"
            if len(embed_fields_values + f"{result}\n") > 1024:
                embed.add_field(name="Probabilities" if is_first_embed else "", value=embed_fields_values, inline=False)
                embed_fields_values = ""
                is_first_embed = False

            embed_fields_values += f"{result}\n"

        embed.add_field(name="Probabilities" if is_first_embed else "", value=embed_fields_values, inline=False)

    @staticmethod
    def _get_plot(craft_probs: dict[int, Decimal]) -> File:
        if len(craft_probs) > 200:
            plt.plot(list(craft_probs.keys()), list(craft_probs.values()), marker='o')  # type: ignore
        else:
            keys_list = list(craft_probs)
            diffs = [keys_list[index + 1] - roll for index, roll in enumerate(keys_list[:-1])]
            bar_width = min(diffs) * 0.9
            plt.bar(list(craft_probs.keys()), list(craft_probs.values()), width=bar_width)  # type: ignore

        plt.title('Roll Probability Distribution')
        plt.ylabel('Probability')
        plt.xlabel('Roll')
        plt.gca().set_axisbelow(True)
        plt.grid(visible=True, alpha=.3)

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        return File(buffer, filename="graph.png")


    class _View(View):
        def __init__(self, craft_prob_cmd: CraftedProbabilityCommand):
            super().__init__(timeout=60)
            self._crafted_prob_cmd = craft_prob_cmd

        # @override
        async def on_timeout(self) -> None:
            # Disable all items on timeout
            for item in self.children:
                self.remove_item(item)
            await self._crafted_prob_cmd._interaction.edit_original_response(view=self)

        async def _click_button(self, button: Button[CraftedProbabilityCommand._View], interaction: Interaction) -> None:
            for item in self.children:
                if isinstance(item, Button):
                    item.disabled = False
            button.disabled = True
            await interaction.edit_original_response(view=self)

        @button(label="Distribution", style=ButtonStyle.green, emoji="🎲", disabled=True)
        async def button_distribution(self, interaction: Interaction, button: Button[Any]) -> None:
            embed = (await self._get_original_embeds(interaction))[0]
            embed.clear_fields()
            self._crafted_prob_cmd._modify_embed_craftprobs(self._crafted_prob_cmd._crafted_util.craft_probs, embed)
            await self._click_button(button, interaction)
            await interaction.edit_original_response(embed=embed, view=self)

        @button(label="Atleast", style=ButtonStyle.green, emoji="📉")
        async def button_atleast(self, interaction: Interaction, button: Button[Any]) -> None:
            embed = (await self._get_original_embeds(interaction))[0]
            embed.clear_fields()
            self._modify_atleast_embed(self._crafted_prob_cmd._crafted_util.craft_probs, embed)
            await self._click_button(button, interaction)
            await interaction.edit_original_response(embed=embed, view=self)

        @button(label="Atmost", style=ButtonStyle.green, emoji="📈")
        async def button_atmost_callback(self, interaction: Interaction, button: Button[Any]) -> None:
            embed = (await self._get_original_embeds(interaction))[0]
            embed.clear_fields()
            self._modify_atmost_embed(self._crafted_prob_cmd._crafted_util.craft_probs, embed)
            await self._click_button(button, interaction)
            await interaction.edit_original_response(embed=embed, view=self)

        @button(label="Plot", style=ButtonStyle.green, emoji="📊")
        async def button_plot_callback(self, interaction: Interaction, button: Button[Any]) -> None:
            await self._click_button(button, interaction)
            await interaction.response.edit_message(
                    embed=None,
                    attachments=[self._crafted_prob_cmd._get_plot(self._crafted_prob_cmd._crafted_util.craft_probs)]
            )


        async def _get_original_embeds(self, interaction: Interaction) -> list[Embed]:
            response = await interaction.original_response()
            return response.embeds

        def _modify_atleast_embed(self, craft_probs: dict[int, Decimal], embed: Embed) -> None:
            embed_cmlr_field_values = ""
            cmlr_probability = 1
            is_first_embed = True
            for IDValue, probability in craft_probs.items():
                one_in_n = round(Decimal(1 / cmlr_probability), 2)
                result = f"Roll: **atleast {IDValue}**, Chance: **{cmlr_probability * 100:.2f}%** (1 in {one_in_n:,})"
                if len(embed_cmlr_field_values + f"{result}\n") > 1024:
                    embed.add_field(name="Probabilities" if is_first_embed else "", value=embed_cmlr_field_values, inline=False)
                    embed_cmlr_field_values = ""
                    is_first_embed = False

                cmlr_probability -= probability
                embed_cmlr_field_values += f"{result}\n"

            embed.add_field(name="Probabilities" if is_first_embed else "", value=embed_cmlr_field_values, inline=False)

        def _modify_atmost_embed(self, craft_probs: dict[int, Decimal], embed: Embed) -> None:
            embed_cml_field_values = ""
            cml_probability = 0
            is_first_embed = True
            for val, prob in craft_probs.items():
                cml_probability += prob
                one_in_n = round(Decimal(1 / cml_probability), 2)
                result = f"Roll: **atmost {val}**, Chance: **{cml_probability * 100:.2f}%** (1 in {one_in_n:,})"
                if len(embed_cml_field_values + f"{result}\n") > 1024:
                    embed.add_field(name="Probabilities" if is_first_embed else "", value=embed_cml_field_values, inline=False)
                    embed_cml_field_values = ""
                    is_first_embed = False

                embed_cml_field_values += f"{result}\n"

            embed.add_field(name="Probabilities" if is_first_embed else "", value=embed_cml_field_values, inline=False)
