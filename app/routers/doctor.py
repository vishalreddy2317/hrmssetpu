from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.doctor import doctor_service
from app.schemas.doctor import DoctorCreate, DoctorUpdate
from app.dependencies.doctor import get_doctor_by_id

router = APIRouter(prefix="/doctor", tags=["Doctor"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_doctor(data: DoctorCreate, db: AsyncSession = Depends(get_db)):
    return await doctor_service.create_doctor(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_doctors(db: AsyncSession = Depends(get_db)):
    return await doctor_service.list_doctors(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_doctor(obj = Depends(get_doctor_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_doctor(id: int, data: DoctorUpdate, db: AsyncSession = Depends(get_db)):
    return await doctor_service.update_doctor(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(id: int, db: AsyncSession = Depends(get_db)):
    return await doctor_service.delete_doctor(db, id)
