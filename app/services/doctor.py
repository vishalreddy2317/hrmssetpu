from app.repositories.doctor import doctor_repository
from app.schemas.doctor import DoctorCreate, DoctorUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class DoctorService:
    def __init__(self):
        self.repo = doctor_repository

    async def create_doctor(self, db: AsyncSession, data: DoctorCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_doctor(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_doctors(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_doctor(self, db: AsyncSession, id: int, data: DoctorUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_doctor(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

doctor_service = DoctorService()
