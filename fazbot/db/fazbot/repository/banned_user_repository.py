from . import Repository
from ..model import BannedUser


class BannedUserRepository(Repository[BannedUser, int]):

    TABLE_NAME = "banned_user"

    # override
    async def create_table(self) -> None:
        await self._db.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                `user_id` BIGINT PRIMARY KEY,
                `reason` TEXT NOT NULL,
                `from` DATETIME NOT NULL,
                `until` DATETIME DEFAULT NULL
            )
            """
        )

    # override
    async def add(self, entity: BannedUser) -> None:
        await self._db.execute(
            f"""
            INSERT INTO {self.TABLE_NAME} (`user_id`, `reason`, `from`, `until`)
            VALUES (?, ?, ?, ?)
            """,
            (entity.user_id, entity.reason, entity.from_, entity.until)
        )

    # override
    async def remove(self, id_: int) -> None:
        await self._db.execute(
            f"""
            DELETE FROM {self.TABLE_NAME}
            WHERE `user_id` = ?
            """,
            (id_,)
        )

    # override
    async def find(self, id_: int) -> BannedUser | None:
        results = await self._db.fetch(
            f"""
            SELECT *
            FROM {self.TABLE_NAME}
            WHERE `user_id` = ?
            """,
            (id_,)
        )
        result = results[0]
        entity = BannedUser.from_dict(result)
        return entity

    # override
    async def find_all(self, ids: list[int]) -> list[BannedUser]:
        results = await self._db.fetch_many(
            f"""
            SELECT *
            FROM {self.TABLE_NAME}
            WHERE `user_id` IN ({", ".join("?" for _ in ids)})
            """,
            (tuple(ids),)
        )
        entities = [BannedUser.from_dict(result) for result in results]
        return entities

    # override
    async def exists(self, id_: int) -> bool:
        return await self.find(id_) is not None

