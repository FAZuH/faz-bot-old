from datetime import datetime
import os
import traceback

from loguru import logger
from nextcord import Colour, Embed, SyncWebhook


class LoggerSetup:

    @classmethod
    def setup(cls, log_directory: str, webhook_url: str, admin_discord_id: int) -> None:
        cls._log_directory = log_directory
        cls._webhook_url = webhook_url
        cls._admin_discord_id = admin_discord_id

        os.makedirs(log_directory, exist_ok=True)
        log_file = os.path.join(log_directory, "fazdb.log")
        logger.add(log_file, level="INFO", rotation="10 MB", compression="zip", enqueue=True, backtrace=True)

        logger.add(sink=cls._critical_discord_sink, filter=cls._discord_filter("CRITICAL"), format=cls._discord_exception_formatter)
        logger.add(sink=cls._error_discord_sink, filter=cls._discord_filter("ERROR"), format=cls._discord_exception_formatter)
        logger.add(sink=cls._warning_discord_sink, filter=cls._discord_filter("WARNING"), format=cls._discord_exception_formatter)
        logger.add(sink=cls._success_discord_sink, filter=cls._discord_filter("SUCCESS"), format=cls._discord_exception_formatter)
        logger.add(sink=cls._info_discord_sink, filter=cls._discord_filter("INFO"), format=cls._discord_exception_formatter)

    @classmethod
    def _critical_discord_sink(cls, message: str) -> None:
        cls._send_embed_to_webhook("CRITICAL", message, colour=Colour.red(), is_admin_ping=True)

    @classmethod
    def _error_discord_sink(cls, message: str) -> None:
        cls._send_embed_to_webhook("ERROR", message, colour=Colour.orange(), is_admin_ping=True)

    @classmethod
    def _warning_discord_sink(cls, message: str) -> None:
        cls._send_embed_to_webhook("WARNING", message, colour=Colour.yellow())
        
    @classmethod
    def _success_discord_sink(cls, message: str) -> None:
        cls._send_embed_to_webhook("SUCCESS", message, colour=Colour.green())

    @classmethod
    def _info_discord_sink(cls, message: str) -> None:
        cls._send_embed_to_webhook("INFO", message, colour=Colour.blue())

    @classmethod
    def _discord_filter(cls, level):
        def filter(record):
            return record["extra"].get("discord", False) and record["level"].name == level
        return filter

    @staticmethod
    def _discord_exception_formatter(record):
        base_format = "<green>{time}</> {message}\n{extra[error_only]}"
        exc = record["exception"]
        if exc is None:
            record["extra"]["error_only"] = ""
        else:
            type_, value, _ = exc
            error_only = "".join(traceback.format_exception_only(type_, value))
            record["extra"]["error_only"] = error_only
        return base_format

    @classmethod
    def _send_embed_to_webhook(
        cls, title: str, description: str, *, colour: Colour | None = None, is_admin_ping: bool = False
    ) -> None:
        webhook = SyncWebhook.from_url(cls._webhook_url)
        embed = Embed(title=title, description=f"```{description[:4090]}```", colour=colour)
        embed.add_field(name="Timestamp", value=f"<t:{int(datetime.now().timestamp())}:R>")

        admin_ping = f"<@{cls._admin_discord_id}>"
        if is_admin_ping:
            webhook.send(content=admin_ping, embed=embed)
        else:
            webhook.send(embed=embed)
