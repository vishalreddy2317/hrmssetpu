from app.repositories.diagnosis import diagnosis_repository
from app.schemas.diagnosis import DiagnosisCreate, DiagnosisUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class DiagnosisService:
    def __init__(self):
        self.repo = diagnosis_repository

    async def create_diagnosis(self, db: AsyncSession, data: DiagnosisCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_diagnosis(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_diagnosiss(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_diagnosis(self, db: AsyncSession, id: int, data: DiagnosisUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_diagnosis(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

diagnosis_service = DiagnosisService()
