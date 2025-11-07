from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.shift import shift_service
from app.schemas.shift import ShiftCreate, ShiftUpdate
from app.dependencies.shift import get_shift_by_id

router = APIRouter(prefix="/shift", tags=["Shift"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_shift(data: ShiftCreate, db: AsyncSession = Depends(get_db)):
    return await shift_service.create_shift(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_shifts(db: AsyncSession = Depends(get_db)):
    return await shift_service.list_shifts(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_shift(obj = Depends(get_shift_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_shift(id: int, data: ShiftUpdate, db: AsyncSession = Depends(get_db)):
    return await shift_service.update_shift(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shift(id: int, db: AsyncSession = Depends(get_db)):
    return await shift_service.delete_shift(db, id)
