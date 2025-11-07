from app.repositories.inventory import inventory_repository
from app.schemas.inventory import InventoryCreate, InventoryUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class InventoryService:
    def __init__(self):
        self.repo = inventory_repository

    async def create_inventory(self, db: AsyncSession, data: InventoryCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_inventory(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_inventorys(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_inventory(self, db: AsyncSession, id: int, data: InventoryUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_inventory(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

inventory_service = InventoryService()
