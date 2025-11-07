from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.message import message_service
from app.schemas.message import MessageCreate, MessageUpdate
from app.dependencies.message import get_message_by_id

router = APIRouter(prefix="/message", tags=["Message"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_message(data: MessageCreate, db: AsyncSession = Depends(get_db)):
    return await message_service.create_message(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_messages(db: AsyncSession = Depends(get_db)):
    return await message_service.list_messages(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_message(obj = Depends(get_message_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_message(id: int, data: MessageUpdate, db: AsyncSession = Depends(get_db)):
    return await message_service.update_message(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(id: int, db: AsyncSession = Depends(get_db)):
    return await message_service.delete_message(db, id)
