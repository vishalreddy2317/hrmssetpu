from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.ward import ward_service
from app.schemas.ward import WardCreate, WardUpdate
from app.dependencies.ward import get_ward_by_id

router = APIRouter(prefix="/ward", tags=["Ward"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_ward(data: WardCreate, db: AsyncSession = Depends(get_db)):
    return await ward_service.create_ward(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_wards(db: AsyncSession = Depends(get_db)):
    return await ward_service.list_wards(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_ward(obj = Depends(get_ward_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_ward(id: int, data: WardUpdate, db: AsyncSession = Depends(get_db)):
    return await ward_service.update_ward(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ward(id: int, db: AsyncSession = Depends(get_db)):
    return await ward_service.delete_ward(db, id)
