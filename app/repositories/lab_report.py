from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.lab_report import LabReport
from app.crud.lab_report import lab_report_crud


class LabReportRepository:
    def __init__(self):
        self.crud = lab_report_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(LabReport))
        return result.scalars().all()


lab_report_repository = LabReportRepository()