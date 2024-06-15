from . import Repository
from ..model import WhitelistedGuild


class WhitelistedGuildRepository(Repository[WhitelistedGuild, int]):

    TABLE_NAME = "whitelisted_guild"

    async def get_all_whitelisted_guilds(self) -> list[int]:
        result = await self._db.fetch(f"""SELECT `guild_id` FROM {self.TABLE_NAME}""")
        guild_ids: list[int] = [
            guild["guild_id"]
            for guild in result
        ]
        return guild_ids

    # override
    async def create_table(self) -> None:
        await self._db.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                `guild_id` BIGINT PRIMARY KEY,
                `guild_name` TEXT NOT NULL,
                `from` DATETIME NOT NULL,
                `until` DATETIME DEFAULT NULL
            )
            """
        )

    # override
    async def insert(self, entity: WhitelistedGuild) -> None:
        await self._db.execute(
            f"""
            INSERT INTO {self.TABLE_NAME} (`guild_id`, `guild_name`, `from`, `until`)
            VALUES (%s, %s, %s, %s)
            """,
            (entity.guild_id, entity.guild_name, entity.from_, entity.until)
        )

    # override
    async def delete(self, id_: int) -> None:
        await self._db.execute(
            f"""
            DELETE FROM {self.TABLE_NAME}
            WHERE `guild_id` = %s
            """,
            (id_,)
        )

    # override
    async def find_one(self, id_: int) -> WhitelistedGuild | None:
        results = await self._db.fetch(
            f"""
            SELECT *
            FROM {self.TABLE_NAME}
            WHERE `guild_id` = %s
            """,
            (id_,)
        )
        result = results[0]
        entity = WhitelistedGuild.from_dict(result)
        return entity

    # override
    async def find_all(self, ids: list[int]) -> list[WhitelistedGuild]:
        results = await self._db.fetch_many(
            f"""
            SELECT *
            FROM {self.TABLE_NAME}
            WHERE `guild_id` IN ({", ".join("%s" for _ in ids)})
            """,
            (tuple(ids),)
        )
        entities = [WhitelistedGuild.from_dict(result) for result in results]
        return entities

    # override
    async def is_exists(self, id_: int) -> bool:
        return await self.find_one(id_) is not None