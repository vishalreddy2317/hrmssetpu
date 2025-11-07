from app.repositories.patient import patient_repository
from app.schemas.patient import PatientCreate, PatientUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class PatientService:
    def __init__(self):
        self.repo = patient_repository

    async def create_patient(self, db: AsyncSession, data: PatientCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_patient(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_patients(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_patient(self, db: AsyncSession, id: int, data: PatientUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_patient(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

patient_service = PatientService()
