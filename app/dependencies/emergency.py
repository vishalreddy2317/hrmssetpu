from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.emergency import emergency_service


async def get_emergency_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await emergency_service.get_emergency(db, id=id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Emergency case not found"
        )
    return obj