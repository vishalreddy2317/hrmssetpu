from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.api_key import APIKey
from app.crud.api_key import api_key_crud


class ApiKeyRepository:
    def __init__(self):
        self.crud = api_key_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(APIKey))
        return result.scalars().all()


api_key_repository = ApiKeyRepository()