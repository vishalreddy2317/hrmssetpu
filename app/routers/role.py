from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.role import role_service
from app.schemas.role import RoleCreate, RoleUpdate
from app.dependencies.role import get_role_by_id

router = APIRouter(prefix="/role", tags=["Role"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_role(data: RoleCreate, db: AsyncSession = Depends(get_db)):
    return await role_service.create_role(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_roles(db: AsyncSession = Depends(get_db)):
    return await role_service.list_roles(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_role(obj = Depends(get_role_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_role(id: int, data: RoleUpdate, db: AsyncSession = Depends(get_db)):
    return await role_service.update_role(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(id: int, db: AsyncSession = Depends(get_db)):
    return await role_service.delete_role(db, id)
