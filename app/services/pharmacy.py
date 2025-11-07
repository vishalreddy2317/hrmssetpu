from app.repositories.pharmacy import pharmacy_repository
from app.schemas.pharmacy import PharmacyCreate, PharmacyUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class PharmacyService:
    def __init__(self):
        self.repo = pharmacy_repository

    async def create_pharmacy(self, db: AsyncSession, data: PharmacyCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_pharmacy(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_pharmacys(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_pharmacy(self, db: AsyncSession, id: int, data: PharmacyUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_pharmacy(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

pharmacy_service = PharmacyService()
