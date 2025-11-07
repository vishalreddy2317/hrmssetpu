from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.nurse import nurse_service
from app.schemas.nurse import NurseCreate, NurseUpdate
from app.dependencies.nurse import get_nurse_by_id

router = APIRouter(prefix="/nurse", tags=["Nurse"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_nurse(data: NurseCreate, db: AsyncSession = Depends(get_db)):
    return await nurse_service.create_nurse(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_nurses(db: AsyncSession = Depends(get_db)):
    return await nurse_service.list_nurses(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_nurse(obj = Depends(get_nurse_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_nurse(id: int, data: NurseUpdate, db: AsyncSession = Depends(get_db)):
    return await nurse_service.update_nurse(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_nurse(id: int, db: AsyncSession = Depends(get_db)):
    return await nurse_service.delete_nurse(db, id)
