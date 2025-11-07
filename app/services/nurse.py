from app.repositories.nurse import nurse_repository
from app.schemas.nurse import NurseCreate, NurseUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class NurseService:
    def __init__(self):
        self.repo = nurse_repository

    async def create_nurse(self, db: AsyncSession, data: NurseCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_nurse(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_nurses(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_nurse(self, db: AsyncSession, id: int, data: NurseUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_nurse(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

nurse_service = NurseService()
