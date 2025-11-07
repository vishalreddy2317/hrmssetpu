from app.repositories.lab_test import lab_test_repository
from app.schemas.lab_test import LabTestCreate, LabTestUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class LabTestService:
    def __init__(self):
        self.repo = lab_test_repository

    async def create_lab_test(self, db: AsyncSession, data: LabTestCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_lab_test(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_lab_tests(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_lab_test(self, db: AsyncSession, id: int, data: LabTestUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_lab_test(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

lab_test_service = LabTestService()
