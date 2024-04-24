# pyright: reportMissingTypeStubs=false
from __future__ import annotations
from typing import TYPE_CHECKING, Any
from discord import Embed

from . import CommandBase
from fazbot.object import WynnEmeralds
from fazbot.util import EmeraldUtil

if TYPE_CHECKING:
    from discord.ext.commands import Context


class ConvertEmeraldCommand(CommandBase):

    def __init__(self, ctx: Context[Any], emerald_string: str) -> None:
        super().__init__(ctx)
        self._emerald_string = emerald_string
        self._emeralds = WynnEmeralds.from_string(emerald_string)
        self._emeralds.simplify()

    async def run(self):
        embed_resp = self._get_embed()
        await self._respond(embed=embed_resp)

    def _get_embed(self) -> Embed:
        set_price_tm, set_price_silverbull = EmeraldUtil.get_set_price(self._emeralds)
        set_price_tm.simplify()
        set_price_silverbull.simplify()
        embed_resp = Embed(title="Emerald Convertor", color=8894804)

        embed_resp.set_thumbnail(url="https://i.ibb.co/2q4KtP2/image-removebg-preview.png")
        embed_resp.description = (f"Converted: **{self._emeralds}**\n" f"Emeralds Total: **{self._emeralds.total}e**")
        embed_resp.add_field(name="TM Set Price", value=f"{set_price_tm}", inline=True)
        embed_resp.add_field(name="Silverbull Set Price", value=f"{set_price_silverbull}", inline=True)
        embed_resp.set_author(name=self._ctx.author.display_name, icon_url=self._ctx.author.display_avatar.url)
        return embed_resp
