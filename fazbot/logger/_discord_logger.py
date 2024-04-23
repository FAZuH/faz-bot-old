from __future__ import annotations
import traceback
from typing import TYPE_CHECKING

from aiohttp import ClientSession
from discord import Colour, Embed, Webhook

if TYPE_CHECKING:
    from . import ConsoleLogger


class DiscordLogger:

    def __init__(self, webhook_url: str, ping_discord_id: int | None = None, console_logger: ConsoleLogger | None = None) -> None:
        """Sends and logs messages into a Discord webhook.

        Args:
            webhook_url (str): The webhook url to send the log message to
            ping_discord_id (int | None, optional): The discord user to ping when a fatal error occurs. Defaults to None.
            console_logger (ConsoleLogger): Console logger instance. Defaults to None
        """
        self._webhook_url = webhook_url
        self._console_logger = console_logger
        self._ping_discord_id = ping_discord_id

    async def success(self, message: str) -> None:
        if self._console_logger:
            self._console_logger.success(message)
        embed = self._get_embed("Success", message, colour=Colour.green())
        await self._send_to_discord(embed)

    async def info(self, message: str) -> None:
        if self._console_logger:
            self._console_logger.info(message)
        embed = self._get_embed("Info", message, colour=Colour.blue())
        await self._send_to_discord(embed)

    async def debug(self, message: str, exception: None | BaseException = None) -> None:
        if self._console_logger:
            self._console_logger.exception(message)
        embed = self._get_embed("Debug", message, exception, Colour.dark_purple())
        await self._send_to_discord(embed)

    async def warning(self, message: str, exception: None | BaseException = None) -> None:
        if self._console_logger:
            self._console_logger.exception(message)
        embed = self._get_embed("Warning", message, exception, Colour.yellow())
        await self._send_to_discord(embed)

    async def exception(self, message: str, exception: None | BaseException = None) -> None:
        if self._console_logger:
            self._console_logger.exception(message)
        embed = self._get_embed("Caught Exception", message, exception, Colour.red())
        await self._send_to_discord(embed)

    async def error(self, message: str, exception: None | BaseException = None) -> None:
        embed = self._get_embed("Fatal Error", message, exception, Colour.red())
        await self._send_to_discord(embed, f"<@{self._ping_discord_id}>" if self._ping_discord_id else None)


    async def _send_to_discord(self, embed: Embed, message: None | str = None) -> None:
        async with ClientSession() as s:
            hook = Webhook.from_url(self._webhook_url, session=s)
            if message:
                await hook.send(message, embed=embed)
            else:
                await hook.send(embed=embed)

    def _get_embed(self, title: str, description: str, exception: BaseException | None = None, colour: Colour | None = None) -> Embed:
        embed = Embed(title=title, description=description, colour=colour)
        if exception:
            tb = traceback.format_exception(exception)
            embed.add_field(name=f"`{exception}`", value=f"```{''.join(tb)}```")
        return embed
