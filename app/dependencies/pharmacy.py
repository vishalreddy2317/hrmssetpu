from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.pharmacy import pharmacy_service

async def get_pharmacy_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await pharmacy_service.get_pharmacy(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pharmacy not found")
    return obj
