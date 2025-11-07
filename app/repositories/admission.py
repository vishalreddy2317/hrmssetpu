from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.admission import Admission
from app.crud.admission import admission_crud


class AdmissionRepository:
    def __init__(self):
        self.crud = admission_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Admission))
        return result.scalars().all()
    
    async def get_active_admissions(self, db: AsyncSession):
        """Get all active admissions"""
        result = await db.execute(
            select(Admission).where(Admission.status == "Active")
        )
        return result.scalars().all()
    
    async def get_by_patient_id(self, db: AsyncSession, patient_id: int):
        """Get all admissions for a patient"""
        result = await db.execute(
            select(Admission).where(Admission.patient_id == patient_id)
        )
        return result.scalars().all()


admission_repository = AdmissionRepository()