from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.api_key import api_key_service
from app.schemas.api_key import APIKeyCreate, APIKeyUpdate
from app.dependencies.api_key import get_api_key_by_id

router = APIRouter(prefix="/api_key", tags=["ApiKey"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_api_key(data: APIKeyCreate, db: AsyncSession = Depends(get_db)):
    return await api_key_service.create_api_key(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_api_keys(db: AsyncSession = Depends(get_db)):
    return await api_key_service.list_api_keys(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_api_key(obj = Depends(get_api_key_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_api_key(id: int, data: APIKeyUpdate, db: AsyncSession = Depends(get_db)):
    return await api_key_service.update_api_key(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_api_key(id: int, db: AsyncSession = Depends(get_db)):
    return await api_key_service.delete_api_key(db, id)
