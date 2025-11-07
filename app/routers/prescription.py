from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.prescription import prescription_service
from app.schemas.prescription import PrescriptionCreate, PrescriptionUpdate
from app.dependencies.prescription import get_prescription_by_id

router = APIRouter(prefix="/prescription", tags=["Prescription"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_prescription(data: PrescriptionCreate, db: AsyncSession = Depends(get_db)):
    return await prescription_service.create_prescription(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_prescriptions(db: AsyncSession = Depends(get_db)):
    return await prescription_service.list_prescriptions(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_prescription(obj = Depends(get_prescription_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_prescription(id: int, data: PrescriptionUpdate, db: AsyncSession = Depends(get_db)):
    return await prescription_service.update_prescription(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prescription(id: int, db: AsyncSession = Depends(get_db)):
    return await prescription_service.delete_prescription(db, id)
