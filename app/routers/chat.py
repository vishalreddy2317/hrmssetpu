from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.chat import chat_service
from app.schemas.chat import ChatCreate, ChatUpdate
from app.dependencies.chat import get_chat_by_id

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_chat(data: ChatCreate, db: AsyncSession = Depends(get_db)):
    return await chat_service.create_chat(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_chats(db: AsyncSession = Depends(get_db)):
    return await chat_service.list_chats(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_chat(obj = Depends(get_chat_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_chat(id: int, data: ChatUpdate, db: AsyncSession = Depends(get_db)):
    return await chat_service.update_chat(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(id: int, db: AsyncSession = Depends(get_db)):
    return await chat_service.delete_chat(db, id)
