from app.repositories.lab_report import lab_report_repository
from app.schemas.lab_report import LabReportCreate, LabReportUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class LabReportService:
    def __init__(self):
        self.repo = lab_report_repository

    async def create_lab_report(self, db: AsyncSession, data: LabReportCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_lab_report(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_lab_reports(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_lab_report(self, db: AsyncSession, id: int, data: LabReportUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_lab_report(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

lab_report_service = LabReportService()
