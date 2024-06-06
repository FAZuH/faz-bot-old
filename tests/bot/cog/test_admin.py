# pyright: reportPrivateUsage=none
from unittest import TestCase
from unittest.mock import MagicMock

from fazbot.bot import DiscordBot
from fazbot.bot.cog import Admin
from fazbot.core import FazBot


class TestAdmin(TestCase):

    def setUp(self) -> None:
        self._core = FazBot()
        self._bot = DiscordBot(self._core)
        self._admin = Admin(self._bot)
        self._admin.setup()

    async def test_cog_check(self) -> None:
        pass

    async def test_cog_application_command_check(self) -> None:
        interaction = MagicMock()
        await self._admin.admin.invoke_callback(interaction)

    async def whisper(self) -> None:
        pass

    async def ban(self) -> None:
        pass

    async def unban(self) -> None:
        pass

    async def echo(self) -> None:
        pass

    async def reload_asset(self) -> None:
        pass

    async def reload_config(self) -> None:
        pass

    async def reload_userdata(self) -> None:
        pass

    async def send(self) -> None:
        pass

    async def sync_guild(self) -> None:
        pass

    async def sync(self) -> None:
        pass

    async def shutdown(self) -> None:
        pass

    async def admin(self) -> None:
        pass

    async def whitelist(self) -> None:
        pass

    def tearDown(self) -> None:
        pass
