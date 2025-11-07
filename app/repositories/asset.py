from app.models.asset import Asset
from app.crud.asset import asset_crud
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class AssetRepository:
    def __init__(self):
        self.crud = asset_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Asset))
        return result.scalars().all()

asset_repository = AssetRepository()
