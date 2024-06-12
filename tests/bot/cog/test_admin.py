# pyright: reportPrivateUsage=none
import asyncio
from unittest import TestCase
from unittest.mock import MagicMock

from fazbot.bot import DiscordBot
from fazbot.bot.cog import Admin
from fazbot.core import FazBot


class TestAdmin(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.interaction = MagicMock()
        cls._core = FazBot()

        with cls._core.enter_fazbotdb() as db:
            eventloop = asyncio.new_event_loop()
            eventloop.run_until_complete(db.create_all_tables())
            eventloop.close()

        cls._bot = DiscordBot(cls._core)
        cls._admin = Admin(cls._bot)
        cls._admin.setup()
        return super().setUpClass()

    def test_cog_check(self) -> None:
        pass

    def test_cog_application_command_check(self) -> None:
        pass

    def whisper(self) -> None:
        pass

    def ban(self) -> None:
        pass

    def unban(self) -> None:
        pass

    def echo(self) -> None:
        pass

    def reload_asset(self) -> None:
        pass

    def reload_config(self) -> None:
        pass

    def send(self) -> None:
        pass

    def sync_guild(self) -> None:
        pass

    def sync(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def admin(self) -> None:
        pass

    def whitelist(self) -> None:
        pass

    def tearDown(self) -> None:
        pass
