from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.technician import Technician
from app.crud.technician import technician_crud


class TechnicianRepository:
    def __init__(self):
        self.crud = technician_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Technician))
        return result.scalars().all()
    
    async def get_available(self, db: AsyncSession):
        """Get available technicians"""
        result = await db.execute(
            select(Technician).where(Technician.is_available == True)
        )
        return result.scalars().all()
    
    async def get_by_specialization(self, db: AsyncSession, specialization: str):
        """Get technicians by specialization"""
        result = await db.execute(
            select(Technician).where(Technician.specialization == specialization)
        )
        return result.scalars().all()


technician_repository = TechnicianRepository()