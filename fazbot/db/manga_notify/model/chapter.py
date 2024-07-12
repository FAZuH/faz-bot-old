from __future__ import annotations
from typing import Any, TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_manga_notify_model import BaseMangaNotifyModel

if TYPE_CHECKING:
    from . import Manga


class Chapter(BaseMangaNotifyModel):
    __tablename__ = "chapter"

    uuid = mapped_column(VARCHAR(36), primary_key=True)
    manga_uuid = mapped_column(VARCHAR(36), ForeignKey("manga.uuid"), nullable=False)

    manga: Mapped[Manga] = relationship("Manga", back_populates="chapters")

    def __init__(self, *, uuid: str, manga_uuid: str, **kw: Any):
        self.uuid = uuid
        self.manga_uuid = manga_uuid
        super().__init__(**kw)
