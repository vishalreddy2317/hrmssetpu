from app.repositories.supplier import supplier_repository
from app.schemas.supplier import SupplierCreate, SupplierUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class SupplierService:
    def __init__(self):
        self.repo = supplier_repository

    async def create_supplier(self, db: AsyncSession, data: SupplierCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_supplier(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_suppliers(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_supplier(self, db: AsyncSession, id: int, data: SupplierUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_supplier(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

supplier_service = SupplierService()
