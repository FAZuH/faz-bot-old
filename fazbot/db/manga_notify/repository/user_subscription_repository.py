from __future__ import annotations
from typing import Sequence, TYPE_CHECKING

from sqlalchemy import select

from ..._base_repository import BaseRepository
from ..model import UserSubscription

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from ..._base_mysql_database import BaseMySQLDatabase


class UserSubscriptionRepository(BaseRepository[UserSubscription, int]):

    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, UserSubscription)

    async def get_users_to_notify(self, *, session: AsyncSession | None = None) -> Sequence[UserSubscription]:
        """
        Retrieve users who have notifications enabled.

        Args:
            session (Optional[AsyncSession]): An optional SQLAlchemy AsyncSession. If not provided, a new session will be created.

        Returns:
            Sequence[UserSubscription]: A list of UserSubscription instances with notifications enabled.
        """
        stmt = select(self.model).where(self.model.is_notify == True)
        async with self.database.enter_async_session() as session:
            result = await session.execute(stmt)
            return result.scalars().all()
