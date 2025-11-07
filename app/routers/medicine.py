from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.medicine import medicine_service
from app.schemas.medicine import MedicineCreate, MedicineUpdate
from app.dependencies.medicine import get_medicine_by_id

router = APIRouter(prefix="/medicine", tags=["Medicine"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_medicine(data: MedicineCreate, db: AsyncSession = Depends(get_db)):
    return await medicine_service.create_medicine(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_medicines(db: AsyncSession = Depends(get_db)):
    return await medicine_service.list_medicines(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_medicine(obj = Depends(get_medicine_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_medicine(id: int, data: MedicineUpdate, db: AsyncSession = Depends(get_db)):
    return await medicine_service.update_medicine(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medicine(id: int, db: AsyncSession = Depends(get_db)):
    return await medicine_service.delete_medicine(db, id)
