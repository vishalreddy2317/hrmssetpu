from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.shift import shift_service

async def get_shift_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await shift_service.get_shift(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shift not found")
    return obj
