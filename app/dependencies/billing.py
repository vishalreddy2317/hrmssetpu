from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.billing import billing_service

async def get_billing_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await billing_service.get_billing(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Billing not found")
    return obj
