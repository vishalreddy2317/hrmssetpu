from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.ward import ward_service

async def get_ward_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await ward_service.get_ward(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ward not found")
    return obj
