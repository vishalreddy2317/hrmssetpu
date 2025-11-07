from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.bed import bed_service

async def get_bed_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await bed_service.get_bed(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bed not found")
    return obj
