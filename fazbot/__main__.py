from __future__ import annotations
import asyncio
from time import sleep

from fazbot.core import FazBot


class Main:

    core = FazBot()

    @staticmethod
    def main() -> None:
        Main.core.start()
        while True:  # keep-alive
            sleep(69_420)

if __name__ == "__main__":
    try:
        Main.main()
    except Exception as e:
        logger = Main.core.logger
        logger.console.exception(str(e))
        asyncio.run(logger.discord.error(f"FATAL ERROR", e))
        exit(1)
