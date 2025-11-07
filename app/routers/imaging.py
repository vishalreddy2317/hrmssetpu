from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.imaging import imaging_service
from app.schemas.imaging import ImagingCreate, ImagingUpdate
from app.dependencies.imaging import get_imaging_by_id

router = APIRouter(prefix="/imaging", tags=["Imaging"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_imaging(data: ImagingCreate, db: AsyncSession = Depends(get_db)):
    return await imaging_service.create_imaging(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_imagings(db: AsyncSession = Depends(get_db)):
    return await imaging_service.list_imagings(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_imaging(obj = Depends(get_imaging_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_imaging(id: int, data: ImagingUpdate, db: AsyncSession = Depends(get_db)):
    return await imaging_service.update_imaging(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_imaging(id: int, db: AsyncSession = Depends(get_db)):
    return await imaging_service.delete_imaging(db, id)
