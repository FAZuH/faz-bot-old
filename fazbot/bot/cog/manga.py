from typing import Literal

import hondana
from hondana.types_.common import LanguageCode
import nextcord
from nextcord import Interaction

from ..errors import *
from ._cog_base import CogBase


class Manga(CogBase):

    @nextcord.slash_command(name="manga", description="Manga commands.")
    async def admin(self, interaction: Interaction) -> None: ...
  
    @admin.subcommand()
    async def subscribe_guild(
            self,
            interaction: Interaction,
            identifier: str,
            language_code: Literal["en", "id"] = "en"
        ) -> None:
        """
        Subscribe to a manga, and send new manga updates to this guild (discord server).

        Args:
            interaction (Interaction): The interaction object representing the user's interaction.
            identifier (str): The identifier of the manga (mangadex_uuid / mangadex_url / mangadex_name).
            language_code (LanguageCode, optional): Translated language of the manga to subscribe. Defaults to "en".
        """
        # Validation
        if not interaction.user:
            raise ValueError("Can't access author user data.")

        if not interaction.guild:
            raise ArgumentValidationFailure("You can only enter this command inside a guild (discord server).")

        guild = interaction.guild
        user = interaction.user
        db = self._bot.app.create_manga_notify_db()

        guild_subs_repo = db.guild_subscription_repository
        user_subs_model = db.user_subscription_repository.model
        manga_model = db.manga_repository.model

        if await guild_subs_repo.is_exists(guild.id) is False:
            raise ArgumentValidationFailure("This guild doesn't have a manga feed registered.")

        mangadex_manga = await self._get_manga(identifier, language_code)
        if mangadex_manga is None:
            raise ArgumentValidationFailure(f"Mangadex manga with id {identifier} not found.")

        # Insert data
        manga = manga_model(uuid=mangadex_manga.id, language_code=language_code, title=mangadex_manga.title)
        user_subs = user_subs_model(id=user.id, name=user.display_name, guild_id=guild.id, is_notify=True, is_notify_guild=True)

        is_subscribed = await db.manga_user_subscription_association.toggle(user_subs, manga)
        if is_subscribed:
            msg = f"Successfully added manga **{manga.title}** to your manga feed on guild **{guild.name}**"
        else:
            msg = f"Successfully removed manga **{manga.title}** from your manga feed on guild **{guild.name}**"

        # Respond
        await self._respond_successful(interaction, msg)

    @subscribe_guild.on_autocomplete("identifier")
    async def _manga_title_autocomplete(self, interaction: Interaction, partial_title: str):
        """
        Autocomplete for manga titles.

        Args:
            interaction (Interaction): The interaction object representing the user's interaction.
            partial_title (str): The partial title of the manga to autocomplete.
        """
        response = interaction.response
        if not partial_title:
            await response.send_autocomplete(["Start typing to get manga autocompletes"])
        manga_title_suggestions = await self._get_manga_title_suggestions(partial_title)
        await response.send_autocomplete(manga_title_suggestions)

    async def _get_manga_title_suggestions(self, partial_title: str) -> list[str]:
        """
        Get manga title suggestions based on a partial title.

        Args:
            partial_title (str): The partial title of the manga to search for.

        Returns:
            list[str]: A list of manga titles that match the partial title.
        """
        async with hondana.Client() as api:
            mangas = await api.manga_list(title=partial_title, limit=10)
        return [manga.title[:100] for manga in mangas.items]

    async def _get_manga(self, id: str, language_code: LanguageCode) -> hondana.Manga | None:
        """
        Get a manga based on the provided identifier and language code.

        Args:
            id (str): The identifier of the manga (mangadex_uuid / mangadex_url / mangadex_name).
            language_code (LanguageCode): The language code of the manga to search for.

        Returns:
            hondana.Manga: The manga that matches the identifier and language code.

        Raises:
            ValueError: If the manga with the provided identifier cannot be found.
        """
        if "https://mangadex" in id:
            id = id.split('/')[-1]
        async with hondana.Client() as api:
            try:
                return await api.get_manga(id)
            except hondana.NotFound:
                pass
            mangas = await api.manga_list(title=id, available_translated_language=[language_code])
            if not mangas.items:
                return None
            return mangas.items[0]
