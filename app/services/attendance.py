from app.repositories.attendance import attendance_repository
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class AttendanceService:
    def __init__(self):
        self.repo = attendance_repository

    async def create_attendance(self, db: AsyncSession, data: AttendanceCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_attendance(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_attendances(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_attendance(self, db: AsyncSession, id: int, data: AttendanceUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_attendance(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

attendance_service = AttendanceService()
