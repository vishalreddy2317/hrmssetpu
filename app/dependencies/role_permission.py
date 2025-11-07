from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.role_permission import role_permission_service

async def get_role_permission_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await role_permission_service.get_role_permission(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RolePermission not found")
    return obj
