from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.test_result import TestResult
from app.crud.test_result import test_result_crud


class TestResultRepository:
    def __init__(self):
        self.crud = test_result_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(TestResult))
        return result.scalars().all()
    
    async def get_by_patient_id(self, db: AsyncSession, patient_id: int):
        """Get test results for a patient"""
        result = await db.execute(
            select(TestResult).where(TestResult.patient_id == patient_id)
        )
        return result.scalars().all()
    
    async def get_abnormal_results(self, db: AsyncSession):
        """Get abnormal test results"""
        result = await db.execute(
            select(TestResult).where(TestResult.status == "Abnormal")
        )
        return result.scalars().all()


test_result_repository = TestResultRepository()