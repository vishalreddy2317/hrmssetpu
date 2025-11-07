from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.emergency import Emergency
from app.crud.emergency import emergency_crud


class EmergencyRepository:
    def __init__(self):
        self.crud = emergency_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Emergency))
        return result.scalars().all()
    
    async def get_by_status(self, db: AsyncSession, status: str):
        """Get emergencies by status"""
        result = await db.execute(
            select(Emergency).where(Emergency.status == status)
        )
        return result.scalars().all()
    
    async def get_by_triage(self, db: AsyncSession, triage_category: str):
        """Get emergencies by triage category"""
        result = await db.execute(
            select(Emergency).where(Emergency.triage_category == triage_category)
        )
        return result.scalars().all()


emergency_repository = EmergencyRepository()