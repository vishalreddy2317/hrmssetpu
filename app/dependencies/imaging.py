from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.imaging import imaging_service

async def get_imaging_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await imaging_service.get_imaging(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Imaging not found")
    return obj
