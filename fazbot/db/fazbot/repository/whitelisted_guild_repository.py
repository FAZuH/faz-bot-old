from . import Repository
from ..model import WhitelistedGuild


class WhitelistedGuildRepository(Repository[WhitelistedGuild, int]):

    TABLE_NAME = "banned_user"

    # override
    async def create_table(self) -> None:
        await self._db.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                guild_id BIGINT PRIMARY KEY,
                guild_name TEXT NOT NULL,
                from DATETIME NOT NULL,
                until DATETIME DEFAULT NULL
            )
            """
        )

    # override
    async def add(self, entity: WhitelistedGuild) -> None:
        await self._db.execute(
            f"""
            INSERT INTO {self.TABLE_NAME} (guild_id, guild_name, from, until)
            VALUES (?, ?, ?, ?)
            """,
            (entity.guild_id, entity.guild_name, entity.from_, entity.until)
        )

    # override
    async def remove(self, id_: int) -> None:
        await self._db.execute(
            f"""
            DELETE FROM {self.TABLE_NAME}
            WHERE guild_id = ?
            """,
            (id_,)
        )

    # override
    async def find(self, id_: int) -> WhitelistedGuild | None:
        results = await self._db.fetch(
            f"""
            SELECT *
            FROM {self.TABLE_NAME}
            WHERE guild_id = ?
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
            WHERE guild_id IN ?
            """,
            (tuple(ids),)
        )
        entities = [WhitelistedGuild.from_dict(result) for result in results]
        return entities

    # override
    async def exists(self, id_: int) -> bool:
        return await self.find(id_) is not None
