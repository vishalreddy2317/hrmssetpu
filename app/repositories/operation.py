from app.models.operation import Operation
from app.crud.operation import operation_crud
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class OperationRepository:
    def __init__(self):
        self.crud = operation_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Operation))
        return result.scalars().all()

operation_repository = OperationRepository()
