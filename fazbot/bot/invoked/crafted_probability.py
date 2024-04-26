# pyright: reportUnknownMemberType=false, reportUnknownArgumentType=false, reportUnknownVariableType=false, reportMissingTypeStubs=false
from __future__ import annotations
from decimal import Decimal
from io import BytesIO
from typing import TYPE_CHECKING, Any

from discord import ButtonStyle, Colour, Embed, Message, errors, File
from discord.ui import button, Button, View
import matplotlib.pyplot as plt


from . import InvokedBase
from fazbot.enum import AssetImageFile
from fazbot.object import WynnIngredientValue
from fazbot.util import CraftedUtil

if TYPE_CHECKING:
    from discord import Interaction
    from discord.ext import commands


class CraftedProbability(InvokedBase):

    INGSTR_DEFAULT = "0,0,0"

    def __init__(self, ctx: commands.Context[Any], ing_strs: list[str]) -> None:
        super().__init__(ctx)
        self._ing_strs = ing_strs
        self._crafted_util = CraftedUtil(self._parse_ings_str(ing_strs))
        self._crafted_util.run()

    async def run(self) -> None:
        embed_resp = self._get_embed(self._ctx, self._crafted_util)
        self._modify_embed_craftprobs(self._crafted_util.craft_probs, embed_resp)

        try:
            view = self._View(self)
            message = await self._respond(embed=embed_resp, view=view, file=self.get_asset_file(AssetImageFile.CRAFTINGTABLE))
            view.message = message
        except errors.HTTPException as e:
            # fallback to sending plot if embed size exceeds maximum size
            if e.code == 50035:
                embed_resp = self._get_plot_embed(self._crafted_util.craft_probs)
                dist_plot = self._get_plot(self._crafted_util.craft_probs)
                await self._ctx.send(embed=embed_resp, file=dist_plot)
            else:
                raise e


    def _get_embed(self, ctx: commands.Context[Any], crafted_util: CraftedUtil) -> Embed:
        embed_resp = Embed(title="Crafteds Probabilites Calculator", color=8894804)
        self.set_embed_thumbnail_with_asset(embed_resp, AssetImageFile.CRAFTINGTABLE)
        embed_resp.set_author(
                name=ctx.author.display_name,
                icon_url=ctx.author.display_avatar.url
        )

        # Embed descriptions
        embed_desc = [f"Ingredients:"]
        for i, ing in enumerate(crafted_util.ingredients, start=1):
            ing_info = f"- `[{i}]`: {ing.min_value} to {ing.max_value}"  # -[nth]: min to max
            ing_info += f", {ing.boost}% boost" if ing.boost != 0 else ""  # Add boost to info if exist
            embed_desc.append(ing_info)
        embed_resp.description = "\n".join(embed_desc)

        # Embed fields
        return embed_resp

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

    def _get_plot_embed(self, craft_probs: dict[int, Decimal]) -> Embed:
        embed = Embed(title="Error", color=Colour.red())

        min_roll = min(craft_probs)
        min_prob = craft_probs[min_roll]
        one_in_n_min = round(Decimal(1 / craft_probs[min_roll]), 2)

        max_roll = max(craft_probs)
        max_prob = craft_probs[max_roll]
        one_in_n_max = round(Decimal(1 / craft_probs[max_roll]), 2)

        embed.description = (
                f"**Embed size exceeds maximum size of 6000. Attaching plot instead.**\n"
                f"- Min Roll: **{min_roll}**, Probability: **{min_prob * 100:.2f}%** (1 in {one_in_n_min:,})\n"
                f"- Max Roll: **{max_roll}**, Probability: **{max_prob * 100:.2f}%** (1 in {one_in_n_max:,})"
        )
        return embed

    def _get_plot(self, craft_probs: dict[int, Decimal]) -> File:
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
        def __init__(self, craft_prob_cmd: CraftedProbability):
            super().__init__(timeout=60)
            self._cmd = craft_prob_cmd

        # @override
        async def on_timeout(self) -> None:
            # Disable all items on timeout
            for item in self.children:
                self.remove_item(item)
            await self.message.edit(view=self)

        @property
        def message(self) -> Message:
            return self._message

        @message.setter
        def message(self, message: Message) -> None:
            self._message = message

        @button(label="Distribution", style=ButtonStyle.green, emoji="🎲", disabled=True)
        async def button_distribution(self, interaction: Interaction, button: Button[Any]) -> None:
            embed = self.message.embeds[0]
            embed.clear_fields()
            self._click_button(button)
            self._cmd._modify_embed_craftprobs(self._cmd._crafted_util.craft_probs, embed)
            await self._respond(interaction, embed, self, [])

        @button(label="Atleast", style=ButtonStyle.green, emoji="📉")
        async def button_atleast(self, interaction: Interaction, button: Button[Any]) -> None:
            embed = self.message.embeds[0]
            embed.clear_fields()
            self._click_button(button)
            self._modify_atleast_embed(self._cmd._crafted_util.craft_probs, embed)
            await self._respond(interaction, embed, self, [])

        @button(label="Atmost", style=ButtonStyle.green, emoji="📈")
        async def button_atmost_callback(self, interaction: Interaction, button: Button[Any]) -> None:
            embed = self.message.embeds[0]
            embed.clear_fields()
            self._click_button(button)
            self._modify_atmost_embed(self._cmd._crafted_util.craft_probs, embed)
            await self._respond(interaction, embed, self, [])

        @button(label="Plot", style=ButtonStyle.green, emoji="📊")
        async def button_plot_callback(self, interaction: Interaction, button: Button[Any]) -> None:
            self._click_button(button)
            dist_plot = self._cmd._get_plot(self._cmd._crafted_util.craft_probs)
            await self._respond(interaction, None, self, [dist_plot])


        def _click_button(self, button: Button[CraftedProbability._View]) -> None:
            for item in self.children:
                if isinstance(item, Button):
                    item.disabled = False
            button.disabled = True

        async def _respond(self, interaction: Interaction, embed: Embed | None, view: View, attachments: list[Any]) -> None:
            await interaction.response.defer()
            await interaction.response.edit_message(embed=embed, view=view, attachments=attachments)

        def _modify_atleast_embed(self, craft_probs: dict[int, Decimal], embed: Embed) -> None:
            field_value = ""
            cmlr_prob = 1
            is_first_embed = True
            for val, prob in craft_probs.items():
                one_in_n = round(Decimal(1 / cmlr_prob), 2)
                line = f"Roll: **atleast {val}**, Chance: **{cmlr_prob * 100:.2f}%** (1 in {one_in_n:,})"
                if len(field_value + f"{line}\n") > 1024:
                    embed.add_field(name="Probabilities" if is_first_embed else "", value=field_value, inline=False)
                    field_value = ""
                    is_first_embed = False

                cmlr_prob -= prob
                field_value += f"{line}\n"

            embed.add_field(name="Probabilities" if is_first_embed else "", value=field_value, inline=False)

        def _modify_atmost_embed(self, craft_probs: dict[int, Decimal], embed: Embed) -> None:
            field_value = ""
            cml_prob = 0
            is_first_embed = True
            for val, prob in craft_probs.items():
                cml_prob += prob
                one_in_n = round(Decimal(1 / cml_prob), 2)
                line = f"Roll: **atmost {val}**, Chance: **{cml_prob * 100:.2f}%** (1 in {one_in_n:,})"
                if len(field_value + f"{line}\n") > 1024:
                    embed.add_field(name="Probabilities" if is_first_embed else "", value=field_value, inline=False)
                    field_value = ""
                    is_first_embed = False

                field_value += f"{line}\n"

            embed.add_field(name="Probabilities" if is_first_embed else "", value=field_value, inline=False)
