from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.supplier import supplier_service
from app.schemas.supplier import SupplierCreate, SupplierUpdate
from app.dependencies.supplier import get_supplier_by_id

router = APIRouter(prefix="/supplier", tags=["Supplier"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_supplier(data: SupplierCreate, db: AsyncSession = Depends(get_db)):
    return await supplier_service.create_supplier(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_suppliers(db: AsyncSession = Depends(get_db)):
    return await supplier_service.list_suppliers(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_supplier(obj = Depends(get_supplier_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_supplier(id: int, data: SupplierUpdate, db: AsyncSession = Depends(get_db)):
    return await supplier_service.update_supplier(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_supplier(id: int, db: AsyncSession = Depends(get_db)):
    return await supplier_service.delete_supplier(db, id)
