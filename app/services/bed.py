from app.repositories.bed import bed_repository
from app.schemas.bed import BedCreate, BedUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class BedService:
    def __init__(self):
        self.repo = bed_repository

    async def create_bed(self, db: AsyncSession, data: BedCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_bed(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_beds(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_bed(self, db: AsyncSession, id: int, data: BedUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_bed(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

bed_service = BedService()
