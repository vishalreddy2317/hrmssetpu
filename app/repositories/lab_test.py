from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.lab_test import LabTest
from app.crud.lab_test import lab_test_crud


class LabTestRepository:
    def __init__(self):
        self.crud = lab_test_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(LabTest))
        return result.scalars().all()


lab_test_repository = LabTestRepository()