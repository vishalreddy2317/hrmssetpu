from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.setting import setting_service

async def get_setting_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await setting_service.get_setting(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Setting not found")
    return obj
