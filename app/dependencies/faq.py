from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.faq import faq_service

async def get_faq_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await faq_service.get_faq(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Faq not found")
    return obj
