from app.repositories.api_key import api_key_repository
from app.schemas.api_key import APIKeyCreate, APIKeyUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class ApiKeyService:
    def __init__(self):
        self.repo = api_key_repository

    async def create_api_key(self, db: AsyncSession, data: APIKeyCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_api_key(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_api_keys(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_api_key(self, db: AsyncSession, id: int, data: APIKeyUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_api_key(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

api_key_service = ApiKeyService()
