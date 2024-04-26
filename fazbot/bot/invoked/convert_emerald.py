from __future__ import annotations
from typing import TYPE_CHECKING, Any

from discord import Embed

from fazbot.enum import AssetImageFile

from . import InvokedBase
from fazbot.object import WynnEmeralds
from fazbot.util import EmeraldUtil

if TYPE_CHECKING:
    from discord.ext import commands


class ConvertEmerald(InvokedBase):

    def __init__(self, ctx: commands.Context[Any], emerald_string: str) -> None:
        super().__init__(ctx)
        self._emerald_string = emerald_string
        self._emeralds = WynnEmeralds.from_string(emerald_string)
        self._emeralds.simplify()

    async def run(self):
        embed_resp = self._get_embed(self._ctx, self._emeralds)
        await self._respond(embed=embed_resp, file=AssetImageFile.LIQUIDEMERALD)

    def _get_embed(self, ctx: commands.Context[Any], emeralds: WynnEmeralds) -> Embed:
        set_price_tm, set_price_silverbull = EmeraldUtil.get_set_price(emeralds)
        set_price_tm.simplify()
        set_price_silverbull.simplify()
        embed_resp = Embed(title="Emerald Convertor", color=8894804)

        self.set_embed_thumbnail_with_asset(embed_resp, AssetImageFile.LIQUIDEMERALD)
        embed_resp.description = (f"Converted: **{emeralds}**\n" f"Emeralds Total: **{emeralds.total}e**")
        embed_resp.add_field(name="TM Set Price", value=f"{set_price_tm}", inline=True)
        embed_resp.add_field(name="Silverbull Set Price", value=f"{set_price_silverbull}", inline=True)
        embed_resp.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        return embed_resp
