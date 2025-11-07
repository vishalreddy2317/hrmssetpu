from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.api_key import api_key_service

async def get_api_key_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await api_key_service.get_api_key(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ApiKey not found")
    return obj
