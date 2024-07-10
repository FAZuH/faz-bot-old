import hashlib
from typing import Any

from .base_fazdb_model import BaseFazdbModel


class UniqueIdModel(BaseFazdbModel):
    __abstract__ = True

    def __init__(self, **kw: Any):
        super().__init__(**kw)
        self.__compute_unique_id()
    
    def __compute_unique_id(self) -> None:
        columns = [
            str(getattr(self, col.name)) for col in self.get_table().columns
            if col.name not in {"unique_id", "datetime"}
        ]
        to_hash = ''.join(columns).encode()
        hashed_columns = hashlib.md5(to_hash).digest()
        self.unique_id = hashed_columns
