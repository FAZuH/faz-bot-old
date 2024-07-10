from __future__ import annotations
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import AsyncGenerator, TYPE_CHECKING
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from sqlalchemy import text

from fazbot.app.properties import Properties
from fazbot.bot._errors import CommandException
from fazbot.bot.cog import Admin
from fazbot.db.fazbot import FazbotDatabase
from fazbot.db.fazbot.model import BannedUser, WhitelistedGuild

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@patch("nextcord.interactions.Interaction")
class TestAdmin(unittest.IsolatedAsyncioTestCase):

    @asynccontextmanager
    async def __mock_enter_db_session(self) -> AsyncGenerator[tuple[FazbotDatabase, AsyncSession], None]:
        async with self.db.enter_session() as session:
            yield self.db, session

    @patch("fazbot.bot.bot.Bot", autospec=True)
    async def asyncSetUp(self, mock_bot: MagicMock) -> None:
        self.mock_bot = mock_bot
        Properties.setup()
        self.db = FazbotDatabase(
            "mysql+aiomysql",
            Properties.MYSQL_USERNAME,
            Properties.MYSQL_PASSWORD,
            Properties.MYSQL_HOST,
            Properties.MYSQL_PORT,
            Properties.FAZDB_DB_NAME
        )
        whitelisted_guild_repo = self.db.whitelisted_guild_repository
        banned_user_repo = self.db.banned_user_repository
        async with self.db.enter_session() as session:
            await whitelisted_guild_repo.create_table(session=session)
            await banned_user_repo.create_table(session=session)
            await session.execute(text(f"TRUNCATE TABLE {whitelisted_guild_repo.table_name}"))
            await session.execute(text(f"TRUNCATE TABLE {banned_user_repo.table_name}"))

        self.admin = Admin(mock_bot)
        # Admin cog overrides
        self.admin._enter_botdb_session = self.__mock_enter_db_session
        return await super().asyncSetUp()

    @unittest.skip("not ready")
    @patch("fazbot.bot.bot.Bot")
    async def test_ban_user_not_banned(self, mock_must_get_user: MagicMock, mock_interaction: MagicMock) -> None:
        """Test if ban() method successfully bans user that's not already banned."""
        self.admin._respond_successful = AsyncMock()
        mock_must_get_user.return_value = self.__get_mock_user()

        await self.admin.ban.invoke_callback(mock_interaction, user_id="10", reason="test")

        self.admin._respond_successful.assert_awaited_once()


    @patch("fazbot.bot._utils.Utils.must_get_user")
    async def test_ban_user_already_banned(self, mock_must_get_user: MagicMock, mock_interaction: MagicMock) -> None:
        """Test if ban() method fails banning user that's already banned."""
        self.admin._respond_error = AsyncMock()  # type: ignore
        mock_must_get_user.return_value = self.__get_mock_user()

        repo = self.db.banned_user_repository
        await repo.insert(self.__insert_dummy_banned_user_entity())
        with self.assertRaises(CommandException):
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
        await self.db.engine.dispose()
        return await super().asyncTearDown()

    @staticmethod
    def __insert_dummy_whitelisted_guild_entity() -> WhitelistedGuild:
        entity = WhitelistedGuild(
            guild_id=10,
            guild_name="test",
            from_=datetime.now().replace(microsecond=0),
            until=(datetime.now() + timedelta(days=1)).replace(microsecond=0)
        )
        return entity

    @staticmethod
    def __insert_dummy_banned_user_entity() -> BannedUser:
        entity = BannedUser(
            user_id=10,
            reason="test",
            from_=datetime.now().replace(microsecond=0),
            until=(datetime.now() + timedelta(days=1)).replace(microsecond=0)
        )
        return entity

    @staticmethod
    def __get_mock_user() -> MagicMock:
        mock_user = MagicMock()
        mock_user.id = 10
        return mock_user
