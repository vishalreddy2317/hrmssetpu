from app.repositories.shift import shift_repository
from app.schemas.shift import ShiftCreate, ShiftUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class ShiftService:
    def __init__(self):
        self.repo = shift_repository

    async def create_shift(self, db: AsyncSession, data: ShiftCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_shift(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_shifts(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_shift(self, db: AsyncSession, id: int, data: ShiftUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_shift(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

shift_service = ShiftService()
