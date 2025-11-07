from app.repositories.ambulance import ambulance_repository
from app.schemas.ambulance import AmbulanceCreate, AmbulanceUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class AmbulanceService:
    def __init__(self):
        self.repo = ambulance_repository

    async def create_ambulance(self, db: AsyncSession, data: AmbulanceCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_ambulance(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_ambulances(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_ambulance(self, db: AsyncSession, id: int, data: AmbulanceUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_ambulance(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

ambulance_service = AmbulanceService()
