from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.notification import notification_service

async def get_notification_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await notification_service.get_notification(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return obj
