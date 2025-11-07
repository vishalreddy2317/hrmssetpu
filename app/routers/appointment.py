from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.appointment import appointment_service
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate
from app.dependencies.appointment import get_appointment_by_id

router = APIRouter(prefix="/appointment", tags=["Appointment"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_appointment(data: AppointmentCreate, db: AsyncSession = Depends(get_db)):
    return await appointment_service.create_appointment(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_appointments(db: AsyncSession = Depends(get_db)):
    return await appointment_service.list_appointments(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_appointment(obj = Depends(get_appointment_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_appointment(id: int, data: AppointmentUpdate, db: AsyncSession = Depends(get_db)):
    return await appointment_service.update_appointment(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(id: int, db: AsyncSession = Depends(get_db)):
    return await appointment_service.delete_appointment(db, id)
