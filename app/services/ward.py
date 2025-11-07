from app.repositories.ward import ward_repository
from app.schemas.ward import WardCreate, WardUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class WardService:
    def __init__(self):
        self.repo = ward_repository

    async def create_ward(self, db: AsyncSession, data: WardCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_ward(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_wards(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_ward(self, db: AsyncSession, id: int, data: WardUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_ward(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

ward_service = WardService()
