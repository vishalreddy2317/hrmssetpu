from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.complaint import complaint_service
from app.schemas.complaint import ComplaintCreate, ComplaintUpdate
from app.dependencies.complaint import get_complaint_by_id

router = APIRouter(prefix="/complaint", tags=["Complaint"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_complaint(data: ComplaintCreate, db: AsyncSession = Depends(get_db)):
    return await complaint_service.create_complaint(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_complaints(db: AsyncSession = Depends(get_db)):
    return await complaint_service.list_complaints(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_complaint(obj = Depends(get_complaint_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_complaint(id: int, data: ComplaintUpdate, db: AsyncSession = Depends(get_db)):
    return await complaint_service.update_complaint(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_complaint(id: int, db: AsyncSession = Depends(get_db)):
    return await complaint_service.delete_complaint(db, id)
