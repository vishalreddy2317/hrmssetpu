from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.payment import payment_service

async def get_payment_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await payment_service.get_payment(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    return obj
