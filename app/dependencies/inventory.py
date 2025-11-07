from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.inventory import inventory_service

async def get_inventory_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await inventory_service.get_inventory(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")
    return obj
