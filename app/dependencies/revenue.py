from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.revenue import revenue_service


async def get_revenue_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await revenue_service.get_revenue(db, id=id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Revenue record not found"
        )
    return obj