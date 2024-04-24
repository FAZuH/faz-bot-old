from unittest import TestCase
from unittest.mock import MagicMock

from fazbot.bot.command import ConvertEmeraldCommand


class TestConvertEmerald(TestCase):

    async def test_convert_emerald(self) -> None:
        interaction = MagicMock()
        convertemerald = ConvertEmeraldCommand(interaction, "100le")
        await convertemerald.run()
        interaction.assert_called_once()
