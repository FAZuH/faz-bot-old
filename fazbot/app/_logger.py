from datetime import datetime
import os
import traceback

from loguru import logger
from nextcord import Colour, Embed, SyncWebhook

from . import LOG_DIR


class Logger:

    _webhook_url: str

    @classmethod
    def setup(cls, webhook_url: str, admin_discord_id: int) -> None:
        cls._webhook_url = webhook_url
        cls._admin_discord_id = admin_discord_id

        os.makedirs(LOG_DIR, exist_ok=True)
        log_file = os.path.join(LOG_DIR, "fazdb.log")
        logger.add(
            log_file,
            level="INFO",
            rotation="10 MB",
            compression="zip",
            enqueue=True,
            backtrace=True,
        )

        logger.add(
            sink=cls.__critical_sink,
            level="CRITICAL",
            enqueue=True,
            format=cls.__discord_formatter
        )
        logger.add(
            sink=cls.__error_sink,
            level="ERROR",
            enqueue=True,
            format=cls.__discord_formatter
        )

    @classmethod
    def __critical_sink(cls, message: str) -> None:
        cls.__send_embed_to_webhook("CRITICAL ERROR", message, Colour.dark_red())

    @classmethod
    def __error_sink(cls, message: str) -> None:
        cls.__send_embed_to_webhook("ERROR", message, Colour.red())
        
    @classmethod
    def __send_embed_to_webhook(cls, title: str, description: str, colour: Colour | None = None) -> None:
        webhook = SyncWebhook.from_url(cls._webhook_url)
        embed = Embed(title=title, description=f"```{description[:4090]}```", colour=colour)
        embed.add_field(name="Timestamp", value=f"<t:{int(datetime.now().timestamp())}:R>")
        admin_ping = f"<@{cls._admin_discord_id}>"
        webhook.send(content=admin_ping, embed=embed)

    @staticmethod
    def __discord_formatter(record):
        base_format = "<green>{time}</> {message}\n{extra[error_only]}"
        exc = record["exception"]
        if exc is None:
            record["extra"]["error_only"] = ""
        else:
            type_, value, _ = exc
            error_only = "".join(traceback.format_exception_only(type_, value))
            record["extra"]["error_only"] = error_only
        return base_format
