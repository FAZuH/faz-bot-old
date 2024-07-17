from typing import TYPE_CHECKING

from .fazbot import FazbotDatabase
from .fazdb import FazdbDatabase


if TYPE_CHECKING:
    from ._base_database import BaseDatabase
    from ._base_mysql_database import BaseMySQLDatabase
    from ._base_model import BaseModel
    from ._base_repository import BaseRepository
