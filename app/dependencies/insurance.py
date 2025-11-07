from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.insurance import insurance_service

async def get_insurance_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await insurance_service.get_insurance(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Insurance not found")
    return obj
