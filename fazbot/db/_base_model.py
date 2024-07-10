from __future__ import annotations
from decimal import Decimal
from typing import Any, Generator, Self, TYPE_CHECKING

from sqlalchemy.orm import DeclarativeBase

if TYPE_CHECKING:
    from sqlalchemy.sql.schema import Table


class BaseModel(DeclarativeBase):
    __abstract__ = True

    @classmethod
    def get_table(cls) -> Table:
        return cls.__table__  # type: ignore

    def clone(self) -> Self:
        return self.__class__(**dict(self.items()))

    def items(self, *, trim_end_underscore: bool = False) -> Generator[tuple[str, Any], None, None]:
        items = vars(self)
        for k, v in items.items():
            if k.startswith('_'):
                continue
            if trim_end_underscore and k.endswith('_'):
                k = k[:-1]
            yield k, v

    def __eq__(self, other: object) -> bool:
        for k, v in self.items():
            v_other = getattr(other, k)
            if v != v_other:
                return False
        return True

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __repr__(self) -> str:
        items = self.items()
        sorted_items = sorted(items, key=lambda x: x[0])
        params = ', '.join(f'{k}={self.__handle_repr_types(v)}' for k, v in sorted_items)
        return f"{self.__class__.__name__}({params})"

    @staticmethod
    def __handle_repr_types(obj: object):
        if isinstance(obj, Decimal):
            return float(obj)
        return obj
