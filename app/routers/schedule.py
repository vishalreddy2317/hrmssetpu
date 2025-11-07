from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.schedule import schedule_service
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate
from app.dependencies.schedule import get_schedule_by_id

router = APIRouter(prefix="/schedule", tags=["Schedule"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_schedule(data: ScheduleCreate, db: AsyncSession = Depends(get_db)):
    return await schedule_service.create_schedule(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_schedules(db: AsyncSession = Depends(get_db)):
    return await schedule_service.list_schedules(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_schedule(obj = Depends(get_schedule_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_schedule(id: int, data: ScheduleUpdate, db: AsyncSession = Depends(get_db)):
    return await schedule_service.update_schedule(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(id: int, db: AsyncSession = Depends(get_db)):
    return await schedule_service.delete_schedule(db, id)
