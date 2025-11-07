from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.equipment import Equipment
from app.crud.equipment import equipment_crud


class EquipmentRepository:
    def __init__(self):
        self.crud = equipment_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Equipment))
        return result.scalars().all()
    
    async def get_available(self, db: AsyncSession):
        """Get all available equipment"""
        result = await db.execute(
            select(Equipment).where(Equipment.status == "Available")
        )
        return result.scalars().all()
    
    async def get_by_category(self, db: AsyncSession, category: str):
        """Get equipment by category"""
        result = await db.execute(
            select(Equipment).where(Equipment.category == category)
        )
        return result.scalars().all()


equipment_repository = EquipmentRepository()