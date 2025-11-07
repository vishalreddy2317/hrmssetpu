from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.hospital import Hospital
from app.crud.hospital import hospital_crud


class HospitalRepository:
    def __init__(self):
        self.crud = hospital_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Hospital))
        return result.scalars().all()
    
    async def get_active(self, db: AsyncSession):
        """Get all active hospitals"""
        result = await db.execute(
            select(Hospital).where(Hospital.is_active == True)
        )
        return result.scalars().all()
    
    async def get_by_code(self, db: AsyncSession, hospital_code: str):
        """Get hospital by code"""
        result = await db.execute(
            select(Hospital).where(Hospital.hospital_code == hospital_code)
        )
        return result.scalar_one_or_none()


hospital_repository = HospitalRepository()