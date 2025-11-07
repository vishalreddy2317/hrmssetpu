from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.room import room_service


async def get_room_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await room_service.get_room(db, id=id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Room not found"
        )
    return obj