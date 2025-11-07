from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.activity_log import ActivityLog
from app.crud.activity_log import activity_log_crud


class ActivityLogRepository:
    def __init__(self):
        self.crud = activity_log_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(ActivityLog))
        return result.scalars().all()


activity_log_repository = ActivityLogRepository()