from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

if TYPE_CHECKING:
    from sqlalchemy.sql.schema import Table


class BaseModel(DeclarativeBase, AsyncAttrs):

    @classmethod
    def get_table(cls) -> Table:
        return cls.__table__  # type: ignore
