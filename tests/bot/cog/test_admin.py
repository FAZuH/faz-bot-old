from __future__ import annotations
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import AsyncGenerator, TYPE_CHECKING
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from fazbot.app.properties import Properties
from fazbot.bot.cog import Admin
from fazbot.bot.errors import ApplicationError
from fazbot.db.fazbot import FazbotDatabase
from fazbot.db.fazbot.model import BannedUser, WhitelistedGuild
from fazbot.db.fazbot.model.whitelist_group import WhitelistGroup

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@patch("nextcord.interactions.Interaction")
class TestAdmin(unittest.IsolatedAsyncioTestCase):

    @asynccontextmanager
    async def _mock_enter_db_session(self) -> AsyncGenerator[tuple[FazbotDatabase, AsyncSession], None]:
        async with self.db.enter_async_session() as session:
            yield self.db, session

    @patch("fazbot.bot.bot.Bot", autospec=True)
    async def asyncSetUp(self, mock_bot: MagicMock) -> None:
        self.mock_bot = mock_bot
        Properties.setup()
        self.db = FazbotDatabase(
            Properties.MYSQL_USERNAME,
            Properties.MYSQL_PASSWORD,
            Properties.MYSQL_HOST,
            Properties.MYSQL_PORT,
            f"{Properties.FAZDB_DB_NAME}_test"
        )

        self.db.create_all()
        await self.db.whitelist_group_repository.truncate()

        self.admin = Admin(mock_bot)
        # Admin cog overrides
        self.admin._enter_botdb_session = self._mock_enter_db_session
        return await super().asyncSetUp()

    @unittest.skip("not ready")
    @patch("fazbot.bot.bot.Bot")
    async def test_ban_user_not_banned(self, mock_must_get_user: MagicMock, mock_interaction: MagicMock) -> None:
        """Test if ban() method successfully bans user that's not already banned."""
        self.admin._respond_successful = AsyncMock()
        mock_must_get_user.return_value = self._get_mock_user()

        await self.admin.ban.invoke_callback(mock_interaction, user_id="10", reason="test")
        self.admin._respond_successful.assert_awaited_once()


    @patch("fazbot.bot._utils.Utils.must_get_user")
    async def test_ban_user_already_banned(self, mock_must_get_user: MagicMock, mock_interaction: MagicMock) -> None:
        """Test if ban() method fails banning user that's already banned."""
        self.admin._respond_error = AsyncMock()  # type: ignore
        mock_must_get_user.return_value = self._get_mock_user()

        repo = self.db.whitelist_group_repository
        await repo.insert(self._get_dummy_banned_user_entity())
        with self.assertRaises(ApplicationError):
            await self.admin.ban.invoke_callback(mock_interaction, user_id="10", reason="test")

    # async def test_unban(self) -> None:
    #     pass
    
    # async def test_echo(self) -> None:
    #     pass
    #
    # async def test_reload_asset(self) -> None:
    #     pass
    #
    # async def test_reload_config(self) -> None:
    #     pass
    #
    # async def test_send(self) -> None:
    #     pass
    #
    # async def test_sync_guild(self) -> None:
    #     pass
    #
    # async def test_sync(self) -> None:
    #     pass
    #
    # async def test_shutdown(self) -> None:
    #     pass
    #
    # async def test_admin(self) -> None:
    #     pass
    #
    # async def test_whitelist(self) -> None:
    #     pass

    async def asyncTearDown(self) -> None:
        await self.db.async_engine.dispose()
        return await super().asyncTearDown()

    @staticmethod
    def _get_dummy_whitelisted_guild_entity() -> WhitelistGroup:
        entity = WhitelistGroup(
            id=10,
            type="guild",
            guild_name="test",
            from_=datetime.now().replace(microsecond=0),
            until=(datetime.now() + timedelta(days=1)).replace(microsecond=0)
        )
        return entity

    @staticmethod
    def _get_dummy_banned_user_entity() -> WhitelistGroup:
        entity = WhitelistGroup(
            id=10,
            type="guild",
            reason="test",
            from_=datetime.now().replace(microsecond=0),
            until=(datetime.now() + timedelta(days=1)).replace(microsecond=0)
        )
        return entity

    @staticmethod
    def _get_mock_user() -> MagicMock:
        mock_user = MagicMock()
        mock_user.id = 10
        return mock_user
