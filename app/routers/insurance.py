from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.insurance import insurance_service
from app.schemas.insurance import InsuranceCreate, InsuranceUpdate
from app.dependencies.insurance import get_insurance_by_id

router = APIRouter(prefix="/insurance", tags=["Insurance"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_insurance(data: InsuranceCreate, db: AsyncSession = Depends(get_db)):
    return await insurance_service.create_insurance(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_insurances(db: AsyncSession = Depends(get_db)):
    return await insurance_service.list_insurances(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_insurance(obj = Depends(get_insurance_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_insurance(id: int, data: InsuranceUpdate, db: AsyncSession = Depends(get_db)):
    return await insurance_service.update_insurance(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_insurance(id: int, db: AsyncSession = Depends(get_db)):
    return await insurance_service.delete_insurance(db, id)
