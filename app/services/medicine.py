from app.repositories.medicine import medicine_repository
from app.schemas.medicine import MedicineCreate, MedicineUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class MedicineService:
    def __init__(self):
        self.repo = medicine_repository

    async def create_medicine(self, db: AsyncSession, data: MedicineCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_medicine(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_medicines(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_medicine(self, db: AsyncSession, id: int, data: MedicineUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_medicine(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

medicine_service = MedicineService()
