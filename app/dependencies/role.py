from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.role import role_service

async def get_role_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await role_service.get_role(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return obj
