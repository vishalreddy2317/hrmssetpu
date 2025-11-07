from app.repositories.radiology import radiology_repository
from app.schemas.radiology import RadiologyCreate, RadiologyUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class RadiologyService:
    def __init__(self):
        self.repo = radiology_repository

    async def create_radiology(self, db: AsyncSession, data: RadiologyCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_radiology(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_radiologys(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_radiology(self, db: AsyncSession, id: int, data: RadiologyUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_radiology(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

radiology_service = RadiologyService()
