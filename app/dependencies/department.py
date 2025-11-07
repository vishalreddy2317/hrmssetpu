from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.department import department_service

async def get_department_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await department_service.get_department(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    return obj
