from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.maintenance import maintenance_service


async def get_maintenance_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await maintenance_service.get_maintenance(db, id=id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Maintenance record not found"
        )
    return obj