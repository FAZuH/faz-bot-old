from __future__ import annotations
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, Literal, override

from ._invoke import Invoke

from nextcord import ButtonStyle, Color, Embed
from nextcord.ui import Button, View, button
from tabulate import tabulate

if TYPE_CHECKING:
    from nextcord import Interaction
    from .. import Bot


class InvokeWorldlist(Invoke):

    def __init__(self, bot: Bot, interaction: Interaction[Any], sort_by: Literal["Player Count", "Time Created"]) -> None:
        self._sort_by: Literal["player", "time"] = "player" if sort_by == "Player Count" else "time"
        super().__init__(bot, interaction) 

    async def run(self):
        self._worlds = await self._bot.fazdb_db.worlds_repository.get_worlds(self._sort_by)
        self._items_per_page = 20
        self._page_count = len(self._worlds) // self._items_per_page + 1

        self._view = self._View(self, self._page_count)
        await self._interaction.send(embed=self._get_embed_page(1), view=self._view)

    def _get_embed_page(self, page: int) -> Embed:
        embed = Embed(title="World List", color=Color.dark_teal())
        time = datetime.now()
        intr = self._interaction
        assert intr.user

        left_index = self._items_per_page * (page - 1)
        right_index = self._items_per_page * page

        worlds = self._worlds[left_index:right_index]
        worldlist = ([w.name, w.player_count, self._timedelta_to_string(time - w.time_created)] for w in worlds)
        embed.description = "```ml\n" + tabulate(worldlist, headers=["World", "Players", "Uptime"], tablefmt="github") + "\n```"

        embed.set_author(name=intr.user.display_name, icon_url=intr.user.display_avatar.url)
        embed.add_field(name="Timestamp", value=f"<t:{int(time.timestamp())}:F>", inline=False)
        embed.add_field(name="Page", value=f"{page} / {self._page_count}", inline=False)
        return embed

    @staticmethod
    def _timedelta_to_string(td: timedelta) -> str:
        hours, remainder = divmod(int(td.total_seconds()), 3600)
        minutes = remainder // 60
        ret = (str(hours) + "h " if hours > 0 else "") + str(minutes) + "m"
        return ret
        
    class _View(View):
        def __init__(self, cmd: InvokeWorldlist, page_count: int):
            super().__init__(timeout=60)
            self._cmd = cmd
            self._page_count = page_count
            self._current_page = 1

        @override
        async def on_timeout(self) -> None:
            await self._cmd._interaction.edit_original_message(view=View(timeout=1))

        @button(style=ButtonStyle.blurple, emoji="⏮️")
        async def first_page_callback(self, button: Button[Any], interaction: Interaction[Any]) -> None:
            await interaction.response.defer()
            self._current_page = 1
            embed = self._cmd._get_embed_page(self._current_page)
            await interaction.edit_original_message(embed=embed)

        @button(style=ButtonStyle.blurple, emoji="◀️")
        async def previous_page_callback(self, button: Button[Any], interaction: Interaction[Any]) -> None:
            await interaction.response.defer()
            self._current_page -= 1
            if self._current_page == 0:
                self._current_page = self._page_count
            embed = self._cmd._get_embed_page(self._current_page)
            await interaction.edit_original_message(embed=embed)

        @button(style=ButtonStyle.red, emoji="⏹️")
        async def stop_(self, button: Button[Any], interaction: Interaction[Any]) -> None:
            await self.on_timeout()

        @button(style=ButtonStyle.blurple, emoji="▶️")
        async def next_page(self, button: Button[Any], interaction: Interaction[Any]) -> None:
            await interaction.response.defer()
            self._current_page += 1
            if self._current_page == (self._page_count + 1):
                self._current_page = 1
            embed = self._cmd._get_embed_page(self._current_page)
            await interaction.edit_original_message(embed=embed)

        @button(style=ButtonStyle.blurple, emoji="⏭️")
        async def last_page(self, button: Button[Any], interaction: Interaction[Any]) -> None:
            await interaction.response.defer()
            self._current_page = self._page_count
            embed = self._cmd._get_embed_page(self._current_page)
            await interaction.edit_original_message(embed=embed)
