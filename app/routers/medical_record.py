from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.medical_record import medical_record_service
from app.schemas.medical_record import MedicalRecordCreate, MedicalRecordUpdate
from app.dependencies.medical_record import get_medical_record_by_id

router = APIRouter(prefix="/medical_record", tags=["MedicalRecord"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_medical_record(data: MedicalRecordCreate, db: AsyncSession = Depends(get_db)):
    return await medical_record_service.create_medical_record(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_medical_records(db: AsyncSession = Depends(get_db)):
    return await medical_record_service.list_medical_records(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_medical_record(obj = Depends(get_medical_record_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_medical_record(id: int, data: MedicalRecordUpdate, db: AsyncSession = Depends(get_db)):
    return await medical_record_service.update_medical_record(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medical_record(id: int, db: AsyncSession = Depends(get_db)):
    return await medical_record_service.delete_medical_record(db, id)
