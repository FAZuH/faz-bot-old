# from datetime import datetime
# from typing import Any
#
# from sqlalchemy import ForeignKey
# from sqlalchemy.dialects.mysql import BIGINT, DATETIME, INTEGER, VARCHAR
# from sqlalchemy.orm import mapped_column
#
# from .base_manga_notify_model import BaseMangaNotifyModel
#
#
# class NotificationHistory(BaseMangaNotifyModel):
#     __tablename__ = "notification_history"
#
#     id = mapped_column(INTEGER, primary_key=True, autoincrement=True)
#     date = mapped_column(DATETIME, nullable=False)
#     user_id = mapped_column(BIGINT, ForeignKey("user_subscription.user_id"), nullable=False)
#     chapter_uuid = mapped_column(VARCHAR(36), ForeignKey("chapter.uuid"), nullable=False)
#
#     def __init__(self, id: int, date: datetime, user_id: int, chapter_uuid: str, **kw: Any):
#         self.id = id
#         self.date = date
#         self.user_id = user_id
#         self.chapter_uuid = chapter_uuid
#         super().__init__(**kw)
