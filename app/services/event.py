from app.repositories.event import event_repository
from app.schemas.event import EventCreate, EventUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class EventService:
    def __init__(self):
        self.repo = event_repository

    async def create_event(self, db: AsyncSession, data: EventCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_event(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_events(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_event(self, db: AsyncSession, id: int, data: EventUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_event(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

event_service = EventService()
