import unittest
from unittest.mock import MagicMock
from unittest import IsolatedAsyncioTestCase

from nextcord import Guild, Interaction, User


class TestManga(IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        self.mock_interaction = MagicMock(spec=Interaction)
        self.mock_user = MagicMock(spec=User)
        self.mock_guild = MagicMock(spec=Guild)
        self.mock_guild.id.return_value = 1
        self.mock_interaction.user = self.mock_user
        self.mock_interaction.guild = self.mock_guild
        return await super().asyncSetUp()

    @unittest.skip('not ready')
    async def test_subscribed_guild_add_new_manga(self) -> None:
        ...

    @unittest.skip('not ready')
    async def test_subscribed_guild_remove_existing_manga(self) -> None:
        ...
