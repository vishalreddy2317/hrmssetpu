from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.event import event_service

async def get_event_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await event_service.get_event(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return obj
