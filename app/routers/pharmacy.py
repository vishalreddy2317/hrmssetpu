from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.pharmacy import pharmacy_service
from app.schemas.pharmacy import PharmacyCreate, PharmacyUpdate
from app.dependencies.pharmacy import get_pharmacy_by_id

router = APIRouter(prefix="/pharmacy", tags=["Pharmacy"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_pharmacy(data: PharmacyCreate, db: AsyncSession = Depends(get_db)):
    return await pharmacy_service.create_pharmacy(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_pharmacys(db: AsyncSession = Depends(get_db)):
    return await pharmacy_service.list_pharmacys(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_pharmacy(obj = Depends(get_pharmacy_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_pharmacy(id: int, data: PharmacyUpdate, db: AsyncSession = Depends(get_db)):
    return await pharmacy_service.update_pharmacy(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pharmacy(id: int, db: AsyncSession = Depends(get_db)):
    return await pharmacy_service.delete_pharmacy(db, id)
