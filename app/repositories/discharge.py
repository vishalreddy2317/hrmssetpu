from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.discharge import Discharge
from app.crud.discharge import discharge_crud


class DischargeRepository:
    def __init__(self):
        self.crud = discharge_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Discharge))
        return result.scalars().all()
    
    async def get_by_patient_id(self, db: AsyncSession, patient_id: int):
        """Get all discharges for a patient"""
        result = await db.execute(
            select(Discharge).where(Discharge.patient_id == patient_id)
        )
        return result.scalars().all()


discharge_repository = DischargeRepository()