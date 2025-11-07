from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.feedback import feedback_service

async def get_feedback_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await feedback_service.get_feedback(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")
    return obj
