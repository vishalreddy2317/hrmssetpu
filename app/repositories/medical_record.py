from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.medical_record import MedicalRecord
from app.crud.medical_record import medical_record_crud


class MedicalRecordRepository:
    def __init__(self):
        self.crud = medical_record_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(MedicalRecord))
        return result.scalars().all()


medical_record_repository = MedicalRecordRepository()