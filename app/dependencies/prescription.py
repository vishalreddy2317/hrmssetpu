from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.prescription import prescription_service

async def get_prescription_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await prescription_service.get_prescription(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found")
    return obj
