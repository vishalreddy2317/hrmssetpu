from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.radiology import radiology_service
from app.schemas.radiology import RadiologyCreate, RadiologyUpdate
from app.dependencies.radiology import get_radiology_by_id

router = APIRouter(prefix="/radiology", tags=["Radiology"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_radiology(data: RadiologyCreate, db: AsyncSession = Depends(get_db)):
    return await radiology_service.create_radiology(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_radiologys(db: AsyncSession = Depends(get_db)):
    return await radiology_service.list_radiologys(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_radiology(obj = Depends(get_radiology_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_radiology(id: int, data: RadiologyUpdate, db: AsyncSession = Depends(get_db)):
    return await radiology_service.update_radiology(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_radiology(id: int, db: AsyncSession = Depends(get_db)):
    return await radiology_service.delete_radiology(db, id)
