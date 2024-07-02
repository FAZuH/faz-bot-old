from __future__ import annotations
import traceback
from typing import TYPE_CHECKING

from aiohttp import ClientSession
from nextcord import Colour, Embed, Webhook

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
        self.__check_console_logger(message)
        embed = self.__get_embed("Success", message, colour=Colour.green())
        await self.__send_to_discord(embed)

    async def info(self, message: str) -> None:
        self.__check_console_logger(message)
        embed = self.__get_embed("Info", message, colour=Colour.blue())
        await self.__send_to_discord(embed)

    async def debug(self, message: str | None = None, exception: None | BaseException = None) -> None:
        self.__check_console_logger(message)
        embed = self.__get_embed("Debug", message, exception, Colour.dark_purple())  # type: ignore
        await self.__send_to_discord(embed)

    async def warning(self, message: str | None = None, exception: None | BaseException = None) -> None:
        self.__check_console_logger(message)
        embed = self.__get_embed("Warning", message, exception, Colour.yellow())  # type: ignore
        await self.__send_to_discord(embed)

    async def exception(self, message: str | None = None, exception: None | BaseException = None) -> None:
        self.__check_console_logger(message)
        embed = self.__get_embed("Caught Exception", message, exception, Colour.red())  # type: ignore
        await self.__send_to_discord(embed)

    async def error(self, message: str | None = None, exception: None | BaseException = None) -> None:
        self.__check_console_logger(message)
        embed = self.__get_embed("Fatal Error", message, exception, Colour.red())  # type: ignore
        await self.__send_to_discord(embed)

    async def __send_to_discord(self, embed: Embed, message: None | str = None) -> None:
        async with ClientSession() as s:
            hook = Webhook.from_url(self._webhook_url, session=s)
            if message:
                await hook.send(message, embed=embed)
            else:
                await hook.send(embed=embed)

    def __get_embed(self, title: str, description: str, exception: BaseException | None = None, colour: Colour | None = None) -> Embed:
        embed = Embed(title=title, description=description, colour=colour)
        if exception:
            tb = traceback.format_exception(exception)
            tb_msg = f"{'\n'.join(tb)}"[:1000]
            tb_msg = f"```{tb_msg}```"
            embed.add_field(name='Traceback', value=tb_msg, inline=False)
        return embed

    def __check_console_logger(self, message: str | None) -> bool:
        if self._console_logger and message:
            return True
        return False
