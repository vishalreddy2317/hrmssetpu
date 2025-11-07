from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.bed import bed_service
from app.schemas.bed import BedCreate, BedUpdate
from app.dependencies.bed import get_bed_by_id

router = APIRouter(prefix="/bed", tags=["Bed"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_bed(data: BedCreate, db: AsyncSession = Depends(get_db)):
    return await bed_service.create_bed(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_beds(db: AsyncSession = Depends(get_db)):
    return await bed_service.list_beds(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_bed(obj = Depends(get_bed_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_bed(id: int, data: BedUpdate, db: AsyncSession = Depends(get_db)):
    return await bed_service.update_bed(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bed(id: int, db: AsyncSession = Depends(get_db)):
    return await bed_service.delete_bed(db, id)
