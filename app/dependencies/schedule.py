from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.schedule import schedule_service

async def get_schedule_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await schedule_service.get_schedule(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
    return obj
