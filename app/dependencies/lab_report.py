from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.lab_report import lab_report_service

async def get_lab_report_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await lab_report_service.get_lab_report(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LabReport not found")
    return obj
