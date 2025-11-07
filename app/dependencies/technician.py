from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.technician import technician_service


async def get_technician_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await technician_service.get_technician(db, id=id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Technician not found"
        )
    return obj