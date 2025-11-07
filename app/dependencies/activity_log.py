from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.activity_log import activity_log_service

async def get_activity_log_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await activity_log_service.get_activity_log(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ActivityLog not found")
    return obj
