from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.lab_test import lab_test_service

async def get_lab_test_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await lab_test_service.get_lab_test(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LabTest not found")
    return obj
