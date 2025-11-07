from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.stock import stock_service

async def get_stock_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await stock_service.get_stock(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock not found")
    return obj
