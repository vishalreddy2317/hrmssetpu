from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.attendance import attendance_service

async def get_attendance_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await attendance_service.get_attendance(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance not found")
    return obj
