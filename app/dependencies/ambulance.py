from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.ambulance import ambulance_service

async def get_ambulance_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await ambulance_service.get_ambulance(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ambulance not found")
    return obj
