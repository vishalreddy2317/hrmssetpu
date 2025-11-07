from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.activity_log import activity_log_service
from app.schemas.activity_log import ActivityLogCreate, ActivityLogUpdate
from app.dependencies.activity_log import get_activity_log_by_id

router = APIRouter(prefix="/activity_log", tags=["ActivityLog"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_activity_log(data: ActivityLogCreate, db: AsyncSession = Depends(get_db)):
    return await activity_log_service.create_activity_log(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_activity_logs(db: AsyncSession = Depends(get_db)):
    return await activity_log_service.list_activity_logs(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_activity_log(obj = Depends(get_activity_log_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_activity_log(id: int, data: ActivityLogUpdate, db: AsyncSession = Depends(get_db)):
    return await activity_log_service.update_activity_log(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity_log(id: int, db: AsyncSession = Depends(get_db)):
    return await activity_log_service.delete_activity_log(db, id)
