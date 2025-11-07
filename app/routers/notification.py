from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.notification import notification_service
from app.schemas.notification import NotificationCreate, NotificationUpdate
from app.dependencies.notification import get_notification_by_id

router = APIRouter(prefix="/notification", tags=["Notification"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_notification(data: NotificationCreate, db: AsyncSession = Depends(get_db)):
    return await notification_service.create_notification(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_notifications(db: AsyncSession = Depends(get_db)):
    return await notification_service.list_notifications(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_notification(obj = Depends(get_notification_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_notification(id: int, data: NotificationUpdate, db: AsyncSession = Depends(get_db)):
    return await notification_service.update_notification(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(id: int, db: AsyncSession = Depends(get_db)):
    return await notification_service.delete_notification(db, id)
