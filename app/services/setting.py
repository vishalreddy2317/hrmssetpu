from app.repositories.setting import setting_repository
from app.schemas.setting import SettingCreate, SettingUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class SettingService:
    def __init__(self):
        self.repo = setting_repository

    async def create_setting(self, db: AsyncSession, data: SettingCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_setting(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_settings(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_setting(self, db: AsyncSession, id: int, data: SettingUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_setting(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

setting_service = SettingService()
