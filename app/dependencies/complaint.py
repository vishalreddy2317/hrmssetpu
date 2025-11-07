from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.complaint import complaint_service

async def get_complaint_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await complaint_service.get_complaint(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")
    return obj
