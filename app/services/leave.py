from app.repositories.leave import leave_repository
from app.schemas.leave import LeaveCreate, LeaveUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class LeaveService:
    def __init__(self):
        self.repo = leave_repository

    async def create_leave(self, db: AsyncSession, data: LeaveCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_leave(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_leaves(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_leave(self, db: AsyncSession, id: int, data: LeaveUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_leave(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

leave_service = LeaveService()
