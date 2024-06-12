from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock

from fazbot.bot.invoke import InvokeConvertEmerald


class TestConvertEmerald(IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.interaction = AsyncMock()
        self.asset = MagicMock()
        self.obj = InvokeConvertEmerald(self.interaction, "100le")
        self.obj.set_assets(self.asset)
        return super().setUp()

    async def test_convert_emerald(self) -> None:
        await self.obj.run()


