from app.models.report import Report
from app.crud.report import report_crud
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class ReportRepository:
    def __init__(self):
        self.crud = report_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Report))
        return result.scalars().all()

report_repository = ReportRepository()
