from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.stock import stock_service
from app.schemas.stock import StockCreate, StockUpdate
from app.dependencies.stock import get_stock_by_id

router = APIRouter(prefix="/stock", tags=["Stock"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_stock(data: StockCreate, db: AsyncSession = Depends(get_db)):
    return await stock_service.create_stock(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_stocks(db: AsyncSession = Depends(get_db)):
    return await stock_service.list_stocks(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_stock(obj = Depends(get_stock_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_stock(id: int, data: StockUpdate, db: AsyncSession = Depends(get_db)):
    return await stock_service.update_stock(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stock(id: int, db: AsyncSession = Depends(get_db)):
    return await stock_service.delete_stock(db, id)
