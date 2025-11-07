from app.repositories.purchase_order import purchaseorder_repository
from app.schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class PurchaseOrderService:
    def __init__(self):
        self.repo = purchaseorder_repository

    async def create_purchase_order(self, db: AsyncSession, data: PurchaseOrderCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_purchase_order(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_purchase_orders(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_purchase_order(self, db: AsyncSession, id: int, data: PurchaseOrderUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_purchase_order(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

purchase_order_service = PurchaseOrderService()
