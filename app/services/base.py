from app.repositories.base import base_repository
from app.schemas.base import BaseCreate, BaseUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class BaseService:
    def __init__(self):
        self.repo = base_repository

    async def create_base(self, db: AsyncSession, data: BaseCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_base(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_bases(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_base(self, db: AsyncSession, id: int, data: BaseUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_base(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

base_service = BaseService()
