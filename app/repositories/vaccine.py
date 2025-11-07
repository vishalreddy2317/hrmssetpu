from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.vaccine import Vaccine
from app.crud.vaccine import vaccine_crud


class VaccineRepository:
    def __init__(self):
        self.crud = vaccine_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Vaccine))
        return result.scalars().all()
    
    async def get_by_patient_id(self, db: AsyncSession, patient_id: int):
        """Get all vaccines for a patient"""
        result = await db.execute(
            select(Vaccine).where(Vaccine.patient_id == patient_id)
        )
        return result.scalars().all()
    
    async def get_by_vaccine_type(self, db: AsyncSession, vaccine_type: str):
        """Get vaccines by type"""
        result = await db.execute(
            select(Vaccine).where(Vaccine.vaccine_type == vaccine_type)
        )
        return result.scalars().all()


vaccine_repository = VaccineRepository()