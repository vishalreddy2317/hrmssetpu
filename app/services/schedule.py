from app.repositories.schedule import schedule_repository
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class ScheduleService:
    def __init__(self):
        self.repo = schedule_repository

    async def create_schedule(self, db: AsyncSession, data: ScheduleCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_schedule(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_schedules(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_schedule(self, db: AsyncSession, id: int, data: ScheduleUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_schedule(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

schedule_service = ScheduleService()
