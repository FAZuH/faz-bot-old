from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint, Table, VARCHAR
from sqlalchemy.dialects.mysql import BIGINT

from .base_manga_notify_model import BaseMangaNotifyModel

manga_user_subscription = Table(
    'manga_user_subscription',
    BaseMangaNotifyModel.metadata,
    Column('manga_uuid', VARCHAR(36), primary_key=True),
    Column('manga_language_code', VARCHAR(15), primary_key=True),
    Column('user_subscription_id', BIGINT, ForeignKey('user_subscription.user_id'), primary_key=True),
    ForeignKeyConstraint(
        ['manga_uuid', 'manga_language_code'],
        ['manga.uuid', 'manga.language_code']
    ),
)
