from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.role_permission import role_permission_service
from app.schemas.role_permission import RolePermissionCreate, RolePermissionUpdate
from app.dependencies.role_permission import get_role_permission_by_id

router = APIRouter(prefix="/role_permission", tags=["RolePermission"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_role_permission(data: RolePermissionCreate, db: AsyncSession = Depends(get_db)):
    return await role_permission_service.create_role_permission(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_role_permissions(db: AsyncSession = Depends(get_db)):
    return await role_permission_service.list_role_permissions(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_role_permission(obj = Depends(get_role_permission_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_role_permission(id: int, data: RolePermissionUpdate, db: AsyncSession = Depends(get_db)):
    return await role_permission_service.update_role_permission(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role_permission(id: int, db: AsyncSession = Depends(get_db)):
    return await role_permission_service.delete_role_permission(db, id)
