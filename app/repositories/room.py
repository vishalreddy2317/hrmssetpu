from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.operation import Operation
from app.crud.operation import operation_crud


class OperationRepository:
    def __init__(self):
        self.crud = operation_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Operation))
        return result.scalars().all()
    
    async def get_scheduled(self, db: AsyncSession):
        """Get all scheduled operations"""
        result = await db.execute(
            select(Operation).where(Operation.status == "Scheduled")
        )
        return result.scalars().all()
    
    async def get_by_patient_id(self, db: AsyncSession, patient_id: int):
        """Get operations for a patient"""
        result = await db.execute(
            select(Operation).where(Operation.patient_id == patient_id)
        )
        return result.scalars().all()


operation_repository = OperationRepository()