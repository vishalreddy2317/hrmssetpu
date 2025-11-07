from app.repositories.prescription import prescription_repository
from app.schemas.prescription import PrescriptionCreate, PrescriptionUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class PrescriptionService:
    def __init__(self):
        self.repo = prescription_repository

    async def create_prescription(self, db: AsyncSession, data: PrescriptionCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_prescription(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_prescriptions(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_prescription(self, db: AsyncSession, id: int, data: PrescriptionUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_prescription(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

prescription_service = PrescriptionService()
