from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.nurse import nurse_service

async def get_nurse_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await nurse_service.get_nurse(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nurse not found")
    return obj
