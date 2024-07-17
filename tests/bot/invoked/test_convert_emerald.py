from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock

from fazbot.bot.invoke import InvokeConvertEmerald


class TestConvertEmerald(IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.interaction = AsyncMock()
        self.asset = MagicMock()

        self.obj = InvokeConvertEmerald(self.interaction, "100le")
        self.obj.set_assets(self.asset)
    
    def test_set_assets(self) -> None:
        # PREPARE
        file = MagicMock()
        filename = "liquidemerald.png"

        # ACT
        self.obj.set_assets({filename: file})

        # ASSERT
        self.assertEqual(file, self.obj.ASSET_LIQUIDEMERALD._file)
        self.assertEqual(filename, self.obj.ASSET_LIQUIDEMERALD.filename)
    #
    # async def test_run(self) -> None:
    #     # PREPARE
    #     embed = MagicMock()
    #     setattr(self.obj, "_InvokeConvertEmerald__get_embed", MagicMock(return_value=embed))
    #
    #     # ACT
    #     await self.obj.run()
    #
    #     # ASSERT
    #     self.obj._interaction.send.assert_called_once_with(embed=embed, file=self.obj.ASSET_LIQUIDEMERALD._file)  # type: ignore
    #
    # def test_get_embed(self) -> None:
    #     # PREPARE
    #     self.interaction.user.display_name = "name"
    #     self.interaction.user.display_avatar.url = "url"
    #
    #     # ACT 
    #     get_embed_method = getattr(self.obj, "_InvokeConvertEmerald__get_embed")
    #     embed = get_embed_method(self.interaction, self.obj._emeralds)
    #     
    #     # ASSERT
    #     self.assertEqual(embed.title, "Emerald Convertor")
    #     self.assertEqual(embed.color.value, 8894804)  # type: ignore
    #     self.assertEqual(embed.description, "Converted: **1stx 36le 0eb 0e**\nEmeralds Total: **409600e**")
    #     self.assertEqual(embed.fields[0].name, "TM Set Price")
    #     self.assertEqual(embed.fields[1].name, "Silverbull Set Price")
    #     self.assertEqual(embed.author.name, "name")
    #     self.assertEqual(embed.author.icon_url, "url")
    #     self.assertEqual(embed.thumbnail.url, "attachment://liquidemerald.png")
