from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.discharge import discharge_service


async def get_discharge_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await discharge_service.get_discharge(db, id=id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Discharge not found"
        )
    return obj