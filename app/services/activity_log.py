from app.repositories.activity_log import activity_log_repository
from app.schemas.activity_log import ActivityLogCreate, ActivityLogUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class ActivityLogService:
    def __init__(self):
        self.repo = activity_log_repository

    async def create_activity_log(self, db: AsyncSession, data: ActivityLogCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_activity_log(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_activity_logs(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_activity_log(self, db: AsyncSession, id: int, data: ActivityLogUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_activity_log(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

activity_log_service = ActivityLogService()
