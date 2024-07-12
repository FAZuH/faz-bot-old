from typing import TYPE_CHECKING

from .fazbot import FazbotDatabase
from .fazdb import FazdbDatabase
from .manga_notify import MangaNotifyDatabase


if TYPE_CHECKING:
    from ._base_async_database import BaseAsyncDatabase
    from ._base_model import BaseModel
    from ._base_repository import BaseRepository
