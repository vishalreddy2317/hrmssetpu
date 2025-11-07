from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.base import base_service

async def get_base_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await base_service.get_base(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Base not found")
    return obj
