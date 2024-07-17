from __future__ import annotations
from decimal import Decimal
from typing import Any, Generator, Self, TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import ColumnProperty, DeclarativeBase, class_mapper

if TYPE_CHECKING:
    from sqlalchemy.sql.schema import Table


class BaseModel(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @classmethod
    def get_table(cls) -> Table:
        return cls.__table__  # type: ignore

    def clone(self) -> Self:
        return self.__class__(**self.to_dict())

    def to_dict(self, *, actual_column_names = True) -> dict[str, Any]:
        if actual_column_names:
            return {
                k: getattr(self, k)
                for k in self.get_column_attribute_names()
            }
        else:
            return {
                getattr(self.__class__, k).name: getattr(self, k)
                for k in self.get_column_attribute_names()
            }

    @classmethod
    def get_column_attribute_names(cls, *, includes_primary_key: bool = True) -> Generator[str, None, None]:
        return (
            p.key for p in class_mapper(cls).iterate_properties
            if isinstance(p, ColumnProperty) and (includes_primary_key or not p.columns[0].primary_key)
        )

    @classmethod
    def get_primarykey_attribute_names(cls) -> Generator[str, None, None]:
        return (
            p.key for p in class_mapper(cls).iterate_properties
            if isinstance(p, ColumnProperty) and p.columns[0].primary_key
        )

    def __eq__(self, other: object) -> bool:
        primary_key = self.get_table().primary_key
        for k, v in self.to_dict().items():
            if k not in primary_key: continue
            v_other = getattr(other, k)
            if v != v_other:
                return False
        return True

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __repr__(self) -> str:
        items = self.to_dict()
        sorted_items = sorted(items.items(), key=lambda x: x[0])
        params = ', '.join(f'{k}={self._handle_repr_types(v)}' for k, v in sorted_items)
        return f"{self.__class__.__name__}({params})"

    @staticmethod
    def _handle_repr_types(obj: object):
        if isinstance(obj, Decimal):
            return float(obj)
        return obj
