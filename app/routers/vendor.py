from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.vendor import vendor_service
from app.schemas.vendor import VendorCreate, VendorUpdate
from app.dependencies.vendor import get_vendor_by_id

router = APIRouter(prefix="/vendor", tags=["Vendor"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_vendor(data: VendorCreate, db: AsyncSession = Depends(get_db)):
    return await vendor_service.create_vendor(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_vendors(db: AsyncSession = Depends(get_db)):
    return await vendor_service.list_vendors(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_vendor(obj = Depends(get_vendor_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_vendor(id: int, data: VendorUpdate, db: AsyncSession = Depends(get_db)):
    return await vendor_service.update_vendor(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vendor(id: int, db: AsyncSession = Depends(get_db)):
    return await vendor_service.delete_vendor(db, id)
