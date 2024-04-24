from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, Any, Sized

from discord import (
    ButtonStyle,
    Colour,
    Embed,
    Interaction,
    Message,
)
from discord.app_commands import Command
from discord.ui import Button, View, button

from . import CommandBase

if TYPE_CHECKING:
    from discord.app_commands import Parameter


class HelpCommand(CommandBase):

    def __init__(self, interaction: Interaction, commands: list[Command[Any, Any, Any]]) -> None:
        super().__init__(interaction)
        self._commands = commands
        self._cmds_per_page = 5
        self._embed_total_pages = 0

    async def run(self) -> None:
        self._embed_total_pages = self._get_embed_total_pages(self._commands)
        embed = self._get_embed_page(self._commands, 1)
        view = self._View(self, self._interaction, self._embed_total_pages, self._commands)
        await self._respond(embed=embed, view=view)

    def _get_embed_page(self, commands: list[Command[Any, ..., Any]], page: int) -> Embed:
        """ Generates embed page for page nth-page """
        embed = Embed(
                title=f"Commands List : Page [{page}/{self._embed_total_pages}]",
                color=Colour.dark_blue(),
                timestamp=datetime.now(),
        )
        embed.set_footer(text="[text] means optional. <text> means required")

        min_idx = self._cmds_per_page * (page - 1)
        max_idx = self._cmds_per_page * page
        for cmd in commands[min_idx:max_idx]:
            parameter_msg = self._get_parameters(cmd.parameters)
            embed.add_field(
                    name=f"/{cmd.qualified_name}{parameter_msg}" ,
                    value=cmd.description or "No brief description given",
                    inline=False
            )
        return embed

    def _get_embed_total_pages(self, commands: Sized) -> int:
        return (len(commands) - 1) // self._cmds_per_page + 1

    def _get_parameters(self, parameters: list[Parameter]) -> str:
        if not parameters:
            # NOTE: case no params
            return ""
        msglist: list[str] = []
        for p in parameters:
            # NOTE: case param disp name, param description
            p_msg = f"{p.display_name}: {p.description}"
            # NOTE: case param isrequired
            p_msg = f"<{p_msg}>" if p.required else p_msg
            msglist.append(p_msg)
        msg = ', '.join(msglist)
        return f" `{msg}`"


    class _View(View):
        def __init__(
            self,
            command: HelpCommand,
            interaction: Interaction,
            help_embed_max_page: int,
            commands: list[Command[Any, ..., Any]]
        ) -> None:
            super().__init__(timeout=120)
            self._interaction = interaction
            self._help_embed_max_page = help_embed_max_page
            self._commands = commands

            self._command = command
            self._current_page = 1
            self._embed_content: None | Embed = None
            self._message: None | Message = None

        async def on_timeout(self) -> None:
            """ Remove all items on timeout """
            for item in self.children:
                self.remove_item(item)
            if self._message is None:
                # TODO: handle
                return
            await self._message.edit(view=self)

        @button(style=ButtonStyle.blurple, emoji="⏮️")
        async def first_page_callback(self, interaction: Interaction, button: Button[Any]) -> None:
            self._current_page = 1
            self._embed_content = self._command._get_embed_page(self._commands, self._current_page)
            await interaction.response.edit_message(embed=self._embed_content)

        @button(style=ButtonStyle.blurple, emoji="◀️")
        async def previous_page_callback(self, interaction: Interaction, button: Button[Any]) -> None:
            self._current_page -= 1
            if self._current_page == 0:
                self._current_page = self._help_embed_max_page
            self._embed_content = self._command._get_embed_page(self._commands, self._current_page)
            await interaction.response.edit_message(embed=self._embed_content)

        @button(style=ButtonStyle.red, emoji="⏹️")
        async def stop_(self, interaction: Interaction, button: Button[Any]) -> None:
            await self.on_timeout()

        @button(style=ButtonStyle.blurple, emoji="▶️")
        async def next_page(self, interaction: Interaction, button: Button[Any]) -> None:
            self._current_page += 1
            if self._current_page == (self._help_embed_max_page + 1):
                self._current_page = 1
            self._embed_content = self._command._get_embed_page(self._commands, self._current_page)
            await interaction.response.edit_message(embed=self._embed_content)

        @button(style=ButtonStyle.blurple, emoji="⏭️")
        async def last_page(self, interaction: Interaction, button: Button[Any]) -> None:
            self._current_page = self._help_embed_max_page
            self._embed_content = self._command._get_embed_page(self._commands, self._current_page)
            await interaction.response.edit_message(embed=self._embed_content)