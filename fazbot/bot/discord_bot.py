# pyright: reportMissingTypeStubs=false
from __future__ import annotations
import asyncio
from threading import Thread
from typing import TYPE_CHECKING

from discord import Activity, ActivityType, errors, Guild, Intents
from discord.ext.commands import Bot as Bot_

from fazbot.enum.userdata_file import UserdataFile

from . import Bot, CogCore

if TYPE_CHECKING:
    from fazbot import App


class DiscordBot(Bot):

    def __init__(self, app: App) -> None:
        self._app = app

        self._synced_guilds: list[Guild] = []
        self._event_loop = asyncio.new_event_loop()

        # set intents
        intents = Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True

        # create bot instance
        self._bot = Bot_('/', intents=intents, help_command=None)

        # create & load cogs
        self._cogs = CogCore(self, self._app)
        self._cogs.load_assets()

        self._discord_bot_thread = Thread(target=self._bot.run, args=(self._app.config.secret.discord.bot_token,), daemon=True)

    def start(self) -> None:
        self._setup()
        self._discord_bot_thread.start()

    def stop(self) -> None:
        self._event_loop.run_until_complete(self._bot.close())

    @property
    def bot(self) -> Bot_:
        return self._bot

    @property
    def synced_guilds(self) -> list[Guild]:
        return self._synced_guilds


    def _setup(self) -> None:
        """ Method to be run on discord bot thread. """
        @self.bot.event
        async def on_ready() -> None:  # type: ignore
            if self.bot.user is not None:
                # TODO: success webhook
                await self._app.logger.discord_logger.success(f"{self.bot.user.display_name} has successfully started.")

            await self.bot.change_presence(activity=Activity(type=ActivityType.playing, name="/help"))

            # Fetch guilds before Cogs.setup()
            for id_ in self._app.userdata.get(UserdataFile.AUTHORIZED_GUILDS):  # type: ignore
                id_: int
                guild = self.bot.get_guild(id_)
                try:
                    if not guild:
                        guild = await self.bot.fetch_guild(id_)
                except errors.Forbidden as e:
                    await self._app.logger.discord_logger.exception(f"An error occurred while fetching guild with ID: {id_}: {e}")
                    continue
                except errors.HTTPException as e:
                    await self._app.logger.discord_logger.exception(f"An HTTP exception occurred while fetching guild with ID: {id_}: {e}")
                    continue
                self._synced_guilds.append(guild)

            await self._cogs.setup(self._synced_guilds)  # Loads all cogs and commands to the client
