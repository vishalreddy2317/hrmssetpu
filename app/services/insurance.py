from app.repositories.insurance import insurance_repository
from app.schemas.insurance import InsuranceCreate, InsuranceUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class InsuranceService:
    def __init__(self):
        self.repo = insurance_repository

    async def create_insurance(self, db: AsyncSession, data: InsuranceCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_insurance(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_insurances(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_insurance(self, db: AsyncSession, id: int, data: InsuranceUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_insurance(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

insurance_service = InsuranceService()
