from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.message import message_service

async def get_message_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await message_service.get_message(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return obj
