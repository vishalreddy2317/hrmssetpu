from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.staff import staff_service


async def get_staff_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await staff_service.get_staff(db, id=id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Staff not found"
        )
    return obj