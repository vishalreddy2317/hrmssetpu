from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.attendance import attendance_service
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate
from app.dependencies.attendance import get_attendance_by_id

router = APIRouter(prefix="/attendance", tags=["Attendance"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_attendance(data: AttendanceCreate, db: AsyncSession = Depends(get_db)):
    return await attendance_service.create_attendance(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_attendances(db: AsyncSession = Depends(get_db)):
    return await attendance_service.list_attendances(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_attendance(obj = Depends(get_attendance_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_attendance(id: int, data: AttendanceUpdate, db: AsyncSession = Depends(get_db)):
    return await attendance_service.update_attendance(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attendance(id: int, db: AsyncSession = Depends(get_db)):
    return await attendance_service.delete_attendance(db, id)
