from app.repositories.vendor import vendor_repository
from app.schemas.vendor import VendorCreate, VendorUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class VendorService:
    def __init__(self):
        self.repo = vendor_repository

    async def create_vendor(self, db: AsyncSession, data: VendorCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_vendor(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_vendors(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_vendor(self, db: AsyncSession, id: int, data: VendorUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_vendor(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

vendor_service = VendorService()
