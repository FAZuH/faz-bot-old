from __future__ import annotations
from time import sleep

from loguru import logger

from fazbot.app import App


class Main:

    app = App()

    @classmethod
    def main(cls) -> None:
        cls.app.start()
        while True:  # keep-alive
            sleep(69_420)


if __name__ == "__main__":
    try:
        with logger.catch(level="CRITICAL", reraise=True):
            Main.main()
    finally:
        Main.app.stop()
