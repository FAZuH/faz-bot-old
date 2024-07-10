from sqlalchemy.dialects.mysql import BINARY, ENUM
from sqlalchemy.orm import Mapped, mapped_column

from .base_fazdb_model import BaseFazdbModel


class CharacterInfo(BaseFazdbModel):
    __tablename__ = "character_info"

    character_uuid: Mapped[bytes] = mapped_column(BINARY(16), nullable=False, primary_key=True)
    uuid: Mapped[bytes] = mapped_column(BINARY(16), nullable=False)
    type: Mapped[str] = mapped_column(ENUM('ARCHER', 'ASSASSIN', 'MAGE', 'SHAMAN', 'WARRIOR'), nullable=False)
