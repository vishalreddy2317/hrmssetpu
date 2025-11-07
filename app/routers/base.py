from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.base import base_service
from app.schemas.base import BaseCreate, BaseUpdate
from app.dependencies.base import get_base_by_id

router = APIRouter(prefix="/base", tags=["Base"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_base(data: BaseCreate, db: AsyncSession = Depends(get_db)):
    return await base_service.create_base(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_bases(db: AsyncSession = Depends(get_db)):
    return await base_service.list_bases(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_base(obj = Depends(get_base_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_base(id: int, data: BaseUpdate, db: AsyncSession = Depends(get_db)):
    return await base_service.update_base(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_base(id: int, db: AsyncSession = Depends(get_db)):
    return await base_service.delete_base(db, id)
