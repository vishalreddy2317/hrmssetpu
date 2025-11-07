from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.user import user_service

async def get_user_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await user_service.get_user(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return obj
