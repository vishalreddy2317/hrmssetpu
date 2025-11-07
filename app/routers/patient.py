from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.patient import patient_service
from app.schemas.patient import PatientCreate, PatientUpdate
from app.dependencies.patient import get_patient_by_id

router = APIRouter(prefix="/patient", tags=["Patient"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_patient(data: PatientCreate, db: AsyncSession = Depends(get_db)):
    return await patient_service.create_patient(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_patients(db: AsyncSession = Depends(get_db)):
    return await patient_service.list_patients(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_patient(obj = Depends(get_patient_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_patient(id: int, data: PatientUpdate, db: AsyncSession = Depends(get_db)):
    return await patient_service.update_patient(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(id: int, db: AsyncSession = Depends(get_db)):
    return await patient_service.delete_patient(db, id)
