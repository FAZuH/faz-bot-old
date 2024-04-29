from __future__ import annotations
from typing import Any

from nextcord import Embed, Interaction

from . import InvokedBase
from fazbot.enum import AssetImageFile
from fazbot.object import WynnEmeralds
from fazbot.util import EmeraldUtil


class ConvertEmerald(InvokedBase):

    def __init__(self, interaction: Interaction[Any], emerald_string: str) -> None:
        super().__init__(interaction)
        self._emerald_string = emerald_string
        self._emeralds = WynnEmeralds.from_string(emerald_string)
        self._emeralds.simplify()

    async def run(self):
        embed_resp = self._get_embed(self._interaction, self._emeralds)
        await self.interaction.send(embed=embed_resp, file=self.get_asset_file(AssetImageFile.LIQUIDEMERALD))

    def _get_embed(self, interaction: Interaction[Any], emeralds: WynnEmeralds) -> Embed:
        set_price_tm, set_price_silverbull = EmeraldUtil.get_set_price(emeralds)
        set_price_tm.simplify()
        set_price_silverbull.simplify()
        embed_resp = Embed(title="Emerald Convertor", color=8894804)

        self.set_embed_thumbnail_with_asset(embed_resp, AssetImageFile.LIQUIDEMERALD)
        embed_resp.description = (f"Converted: **{emeralds}**\n" f"Emeralds Total: **{emeralds.total}e**")
        embed_resp.add_field(name="TM Set Price", value=f"{set_price_tm}", inline=True)
        embed_resp.add_field(name="Silverbull Set Price", value=f"{set_price_silverbull}", inline=True)
        if interaction.user:
            embed_resp.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        return embed_resp
