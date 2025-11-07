from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.chat import chat_service

async def get_chat_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await chat_service.get_chat(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    return obj
