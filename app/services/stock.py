from app.repositories.stock import stock_repository
from app.schemas.stock import StockCreate, StockUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class StockService:
    def __init__(self):
        self.repo = stock_repository

    async def create_stock(self, db: AsyncSession, data: StockCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_stock(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_stocks(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_stock(self, db: AsyncSession, id: int, data: StockUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_stock(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

stock_service = StockService()
