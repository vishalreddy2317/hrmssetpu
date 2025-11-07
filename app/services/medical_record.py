from app.repositories.medical_record import medical_record_repository
from app.schemas.medical_record import MedicalRecordCreate, MedicalRecordUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class MedicalRecordService:
    def __init__(self):
        self.repo = medical_record_repository

    async def create_medical_record(self, db: AsyncSession, data: MedicalRecordCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_medical_record(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_medical_records(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_medical_record(self, db: AsyncSession, id: int, data: MedicalRecordUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_medical_record(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

medical_record_service = MedicalRecordService()
