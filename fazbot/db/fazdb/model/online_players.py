from sqlalchemy.dialects.mysql import BINARY, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from .base_fazdb_model import BaseFazdbModel


class OnlinePlayers(BaseFazdbModel):
    __tablename__ = "online_players"

    uuid: Mapped[bytes] = mapped_column(BINARY(16), primary_key=True, nullable=False)
    server: Mapped[str] = mapped_column(VARCHAR(10), nullable=False)
