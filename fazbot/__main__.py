from __future__ import annotations
import asyncio
from time import sleep
from typing import TYPE_CHECKING

from fazbot.core import FazBot

if TYPE_CHECKING:
    from fazbot import Core


class Main:
    """ <<public static>> """

    app: Core = FazBot()

    @staticmethod
    def main() -> None:
        Main.app.start()
        while True:  # keep-alive
            sleep(69_420)


if __name__ == "__main__":
    main = Main()
    try:
        main.main()
    except Exception as e:
        asyncio.run(Main.app.logger.discord_logger.error(f"FATAL ERROR", e))
        exit(1)
