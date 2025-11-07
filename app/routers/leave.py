from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.leave import leave_service
from app.schemas.leave import LeaveCreate, LeaveUpdate
from app.dependencies.leave import get_leave_by_id

router = APIRouter(prefix="/leave", tags=["Leave"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_leave(data: LeaveCreate, db: AsyncSession = Depends(get_db)):
    return await leave_service.create_leave(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_leaves(db: AsyncSession = Depends(get_db)):
    return await leave_service.list_leaves(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_leave(obj = Depends(get_leave_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_leave(id: int, data: LeaveUpdate, db: AsyncSession = Depends(get_db)):
    return await leave_service.update_leave(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_leave(id: int, db: AsyncSession = Depends(get_db)):
    return await leave_service.delete_leave(db, id)
