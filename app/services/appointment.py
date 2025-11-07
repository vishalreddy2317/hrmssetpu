from app.repositories.appointment import appointment_repository
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class AppointmentService:
    def __init__(self):
        self.repo = appointment_repository

    async def create_appointment(self, db: AsyncSession, data: AppointmentCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_appointment(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_appointments(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_appointment(self, db: AsyncSession, id: int, data: AppointmentUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_appointment(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

appointment_service = AppointmentService()
