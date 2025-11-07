from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.event import event_service
from app.schemas.event import EventCreate, EventUpdate
from app.dependencies.event import get_event_by_id

router = APIRouter(prefix="/event", tags=["Event"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_event(data: EventCreate, db: AsyncSession = Depends(get_db)):
    return await event_service.create_event(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_events(db: AsyncSession = Depends(get_db)):
    return await event_service.list_events(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_event(obj = Depends(get_event_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_event(id: int, data: EventUpdate, db: AsyncSession = Depends(get_db)):
    return await event_service.update_event(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(id: int, db: AsyncSession = Depends(get_db)):
    return await event_service.delete_event(db, id)
