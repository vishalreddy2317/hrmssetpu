from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.vaccine import vaccine_service


async def get_vaccine_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await vaccine_service.get_vaccine(db, id=id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Vaccine record not found"
        )
    return obj