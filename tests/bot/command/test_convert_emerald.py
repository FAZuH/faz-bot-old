from unittest import TestCase
from unittest.mock import MagicMock

from fazbot.bot.invoked import ConvertEmerald


class TestConvertEmerald(TestCase):

    async def test_convert_emerald(self) -> None:
        ctx = MagicMock()
        convertemerald = ConvertEmerald(ctx, "100le")
        await convertemerald.run()
        ctx.assert_called_once()
