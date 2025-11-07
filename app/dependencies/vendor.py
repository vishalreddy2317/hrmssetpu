from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.vendor import vendor_service

async def get_vendor_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await vendor_service.get_vendor(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")
    return obj
