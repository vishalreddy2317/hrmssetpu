from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.medical_record import medical_record_service

async def get_medical_record_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await medical_record_service.get_medical_record(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MedicalRecord not found")
    return obj
