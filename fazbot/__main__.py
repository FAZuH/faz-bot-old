from __future__ import annotations
import asyncio
from time import sleep
from typing import TYPE_CHECKING

from fazbot.app import FazBot

if TYPE_CHECKING:
    from fazbot import App


class Main:
    """ <<public static>> """

    app: App = FazBot()

    @staticmethod
    def main() -> None:
        Main.app.start()

        while True:
            inp = input()
            if inp == "exit":
                Main.app.stop()
                exit(0)
            sleep(0.1)


if __name__ == "__main__":
    main = Main()
    try:
        main.main()
    except Exception as e:
        asyncio.run(Main.app.logger.discord_logger.error(f"FATAL ERROR", e))
        exit(1)
