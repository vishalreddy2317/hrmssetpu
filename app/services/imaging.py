from app.repositories.imaging import imaging_repository
from app.schemas.imaging import ImagingCreate, ImagingUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class ImagingService:
    def __init__(self):
        self.repo = imaging_repository

    async def create_imaging(self, db: AsyncSession, data: ImagingCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_imaging(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_imagings(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_imaging(self, db: AsyncSession, id: int, data: ImagingUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_imaging(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

imaging_service = ImagingService()
