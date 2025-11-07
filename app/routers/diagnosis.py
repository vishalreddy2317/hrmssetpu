from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.diagnosis import diagnosis_service
from app.schemas.diagnosis import DiagnosisCreate, DiagnosisUpdate
from app.dependencies.diagnosis import get_diagnosis_by_id

router = APIRouter(prefix="/diagnosis", tags=["Diagnosis"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_diagnosis(data: DiagnosisCreate, db: AsyncSession = Depends(get_db)):
    return await diagnosis_service.create_diagnosis(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_diagnosiss(db: AsyncSession = Depends(get_db)):
    return await diagnosis_service.list_diagnosiss(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_diagnosis(obj = Depends(get_diagnosis_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_diagnosis(id: int, data: DiagnosisUpdate, db: AsyncSession = Depends(get_db)):
    return await diagnosis_service.update_diagnosis(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diagnosis(id: int, db: AsyncSession = Depends(get_db)):
    return await diagnosis_service.delete_diagnosis(db, id)
