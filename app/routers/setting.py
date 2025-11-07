from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.setting import setting_service
from app.schemas.setting import SettingCreate, SettingUpdate
from app.dependencies.setting import get_setting_by_id

router = APIRouter(prefix="/setting", tags=["Setting"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_setting(data: SettingCreate, db: AsyncSession = Depends(get_db)):
    return await setting_service.create_setting(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_settings(db: AsyncSession = Depends(get_db)):
    return await setting_service.list_settings(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_setting(obj = Depends(get_setting_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_setting(id: int, data: SettingUpdate, db: AsyncSession = Depends(get_db)):
    return await setting_service.update_setting(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_setting(id: int, db: AsyncSession = Depends(get_db)):
    return await setting_service.delete_setting(db, id)
