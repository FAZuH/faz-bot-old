from __future__ import annotations
import asyncio
from datetime import datetime, timedelta
from typing import Iterable, TYPE_CHECKING, override

from hondana.client import Client
from loguru import logger
import nextcord

from .itask import ITask

if TYPE_CHECKING:
    import hondana
    from fazbot.app import App
    from fazbot.db.manga_notify.model import *


class TaskMangaNotify(ITask):

    def __init__(self, app: App) -> None:
        self._app = app

        self._event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._event_loop)

        self._db = app.create_manga_notify_db()
        self._latest_run = datetime.now()
        self._start_time = datetime.now()
        self._api = Client()

        self._previously_pinged_chapters: set[str] = set()

    @override
    def setup(self) -> None:
        self._db.create_all()
        
    @override
    def teardown(self) -> None:
        logger.info(f"Tearing down {self.name}.")
        self._db.engine.dispose()
        if self._event_loop.is_running():
            asyncio.run_coroutine_threadsafe(self._async_teardown(), self._event_loop).result()
        else:
            asyncio.run(self._api.close())
        self._event_loop.close()

    async def _async_teardown(self) -> None:
        await self._api.close()
        await self._db.teardown()

    @override
    def run(self) -> None:
        with logger.catch(level="ERROR"):
            logger.info(f"Running {self.name}.")
            asyncio.run_coroutine_threadsafe(self._run(), self._event_loop).result()
        self._latest_run = datetime.now()
        logger.info(f"Finished running {self.name}.")

    async def _run(self) -> None:
        all_new_chapters = await self._get_all_new_chapters()
        guild_subscriptions = set(await self._db.guild_subscription_repository.select_all())
        await self._notify_guilds(guild_subscriptions, all_new_chapters)

    async def _notify_guilds(self, guild_subscriptions: set[GuildSubscription], new_chapters: set[hondana.Chapter]) -> None:
        """
        Notify guilds about new chapters based on their subscriptions.

        This method sends notifications to Discord channels of guild subscriptions
        for new chapters that have been updated since the last run. It fetches the
        appropriate channel, determines users to ping, and sends notifications 
        using `_notify_target`.

        Args:
            guild_subscriptions (Iterable[GuildSubscription]):
                Iterable of GuildSubscription objects representing guilds to notify.
            new_chapters (set[hondana.Chapter]):
                Set of new Chapter objects to notify about.
        """
        logger.info(f"Notifying {len(guild_subscriptions)} guilds about {len(new_chapters)} new chapters.")
        self._previously_pinged_chapters = set()
        for guild in guild_subscriptions:
            with logger.catch(ValueError, level='ERROR'):
                channel = await self._get_sendable_channel(guild.channel_id)

            for ch in new_chapters:
                if not ch.manga_id: continue
                with logger.catch(ValueError, level='ERROR'):
                    users_to_ping = guild.get_users_to_ping(ch.manga_id)

                await self._notify_target(channel, ch, users_to_ping)
                self._previously_pinged_chapters.add(ch.id)

    async def _get_sendable_channel(self, channel_id: int) -> nextcord.abc.MessageableChannel:
        """
        Fetches a sendable Discord channel by its ID.

        Args:
            channel_id (int): The ID of the channel to fetch.

        Raises:
            ValueError: If the fetched channel is not a messageable channel.

        Returns:
            nextcord.abc.MessageableChannel: The fetched channel if it is messageable.
        """
        with self._app.enter_bot() as bot:
            channel = await bot.client.fetch_channel(channel_id)
        if not isinstance(channel, nextcord.abc.Messageable):
            raise ValueError(f"Invalid channel_id {channel_id}.")
        return channel

    async def _notify_target(
        self, 
        target: nextcord.abc.Messageable, 
        chapter: hondana.Chapter, 
        to_ping: Iterable[int] | int | None = None
    ) -> None:
        """
        Sends a notification about a new chapter to a Discord message target.

        Args:
            target (nextcord.abc.Messageable):
                The Discord messageable target to send the notification to.
            chapter (hondana.Chapter):
                The chapter information to be included in the notification.
            to_ping (Optional[Union[Iterable[int], int]]):
                The user(s) to ping in the notification. Can be an integer representing a single user ID, an iterable of user IDs, or None.
        """
        pings = None
        if isinstance(to_ping, Iterable):
            pings = ", ".join(f"<@{id_}>" for id_ in to_ping)
        elif isinstance(to_ping, int):
            pings = str(to_ping)

        embed = self._get_embed_message(chapter)
        await target.send(content=pings, embed=embed)
        logger.info(f"Notified target {target} about chapter {chapter}.")

    @staticmethod
    def _get_embed_message(chapter: hondana.Chapter) -> nextcord.Embed:
        """
        Generate an embed message for a new manga chapter notification.

        Args:
            chapter (hondana.Chapter): The Chapter object containing information about the new chapter.

        Returns:
            nextcord.Embed: Embed object containing formatted information about the new chapter.
        """
        embed = nextcord.Embed()
        embed.title = "Mangadex Update!"
        embed.colour = nextcord.Colour.dark_orange()
        manga_title = chapter.manga.title if chapter.manga else 'ERROR'
        manga_url = chapter.manga.url if chapter.manga else None
        embed.description = f"### New [{manga_title}]({manga_url}) chapter is out!"

        msgs: list[str] = [
            ":scroll:"      + f" ` Chapter   :` **{chapter.chapter}**",
            ":book:"        + f" ` Title     :` **{chapter.title}**",
            ":label:"       + f" ` Pages     :` **{chapter.pages}**",
            ":earth_asia:"  + f" ` Language  :` **{chapter.translated_language}**",
            ":alarm_clock:" + f" ` Timestamp :` **<t:{int(chapter.updated_at.timestamp())}:R>**"
        ]
        msg = '\n'.join(msgs)
        embed.add_field(name="Chapter Info", value=msg, inline=False)

        embed.add_field(name="Link", value=f"**[Click Here!]({chapter.url})**", inline=False)
        return embed

    async def _get_new_chapters(self, manga: Manga) -> set[hondana.Chapter]:
        """
        Retrieve the chapter feed for a given manga and return new chapters since the last run.

        Args:
            manga (Manga): The Manga object for which to retrieve the chapter feed.

        Returns:
            Set[Chapter]: A set of new chapters updated since the last run.
        """
        chapter_feed = await self._api.chapter_list(
            manga=manga.uuid,
            translated_language=[manga.language_code],
            updated_at_since=datetime.now() - timedelta(seconds=2 * self.interval)
        )
        new_chapters: set[hondana.Chapter] = set()
        for ch in chapter_feed.items:
            if ch.id in self._previously_pinged_chapters:
                continue
            if ch.updated_at > self._latest_run:
                new_chapters.add(ch)
        logger.info(f"Found {len(new_chapters)} new chapters for manga {manga.uuid}.")
        return new_chapters

    async def _get_all_new_chapters(self) -> set[hondana.Chapter]:
        """
        Retrieve new chapters for all mangas that have been updated since the last run.

        This method checks all mangas in the database and collects new chapters that 
        have been updated since the last run. It avoids duplicate checks by maintaining 
        a set of checked manga UUIDs.

        Returns:
            set[hondana.Chapter]: A set of new chapters across all mangas that have been 
            updated since the last run.
        """
        checked_manga: set[str] = set()
        ret: set[hondana.Chapter] = set()

        mangas = await self._db.manga_repository.select_all()

        for manga in mangas:
            if manga.uuid in checked_manga:
                continue

            new_chapters = await self._get_new_chapters(manga)
            if not new_chapters: continue

            checked_manga.add(manga.uuid)
            ret.update(new_chapters)

        logger.info(f"Retrieved {len(ret)} new chapters.")
        return ret

    @property
    @override
    def first_delay(self) -> float:
        return 5.0

    @property
    @override
    def interval(self) -> float:
        return 300.0

    @property
    @override
    def latest_run(self) -> datetime:
        return self._latest_run

    @property
    @override
    def name(self) -> str:
        return "TaskMangaNotify"
