from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.staff import Staff
from app.crud.staff import staff_crud


class StaffRepository:
    def __init__(self):
        self.crud = staff_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Staff))
        return result.scalars().all()
    
    async def get_active(self, db: AsyncSession):
        """Get all active staff"""
        result = await db.execute(
            select(Staff).where(Staff.is_active == True)
        )
        return result.scalars().all()
    
    async def get_by_designation(self, db: AsyncSession, designation: str):
        """Get staff by designation"""
        result = await db.execute(
            select(Staff).where(Staff.designation == designation)
        )
        return result.scalars().all()


staff_repository = StaffRepository()