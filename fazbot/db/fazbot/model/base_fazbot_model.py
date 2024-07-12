from sqlalchemy import MetaData

from ..._base_model import BaseModel


class BaseFazbotModel(BaseModel):
    __abstract__ = True
    metadata = MetaData()
