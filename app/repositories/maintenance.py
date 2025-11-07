from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.maintenance import Maintenance
from app.crud.maintenance import maintenance_crud


class MaintenanceRepository:
    def __init__(self):
        self.crud = maintenance_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Maintenance))
        return result.scalars().all()
    
    async def get_by_equipment_id(self, db: AsyncSession, equipment_id: int):
        """Get maintenance logs for equipment"""
        result = await db.execute(
            select(Maintenance).where(Maintenance.equipment_id == equipment_id)
        )
        return result.scalars().all()
    
    async def get_pending(self, db: AsyncSession):
        """Get pending maintenance"""
        result = await db.execute(
            select(Maintenance).where(Maintenance.status == "Pending")
        )
        return result.scalars().all()


maintenance_repository = MaintenanceRepository()