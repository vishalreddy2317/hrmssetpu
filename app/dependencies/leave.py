from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.leave import leave_service

async def get_leave_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await leave_service.get_leave(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave not found")
    return obj
