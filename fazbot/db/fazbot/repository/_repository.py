from abc import ABC, abstractmethod

from ... import DatabaseQuery


class Repository[E, ID](ABC):

    TABLE_NAME: str

    def __init__(self, db: DatabaseQuery) -> None:
        self._db = db

    @abstractmethod
    async def create_table(self) -> None: ...

    @abstractmethod
    async def add(self, entity: E) -> None: ...

    @abstractmethod
    async def remove(self, id_: ID) -> None: ...

    @abstractmethod
    async def find(self, id_: ID) -> E | None: ...

    @abstractmethod
    async def find_all(self, ids: list[ID]) -> list[E]: ...

    @abstractmethod
    async def exists(self, id_: ID) -> bool: ...
