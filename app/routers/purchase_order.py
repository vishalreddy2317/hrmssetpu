from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.purchase_order import purchase_order_service
from app.schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderUpdate
from app.dependencies.purchase_order import get_purchase_order_by_id

router = APIRouter(prefix="/purchase_order", tags=["PurchaseOrder"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_purchase_order(data: PurchaseOrderCreate, db: AsyncSession = Depends(get_db)):
    return await purchase_order_service.create_purchase_order(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_purchase_orders(db: AsyncSession = Depends(get_db)):
    return await purchase_order_service.list_purchase_orders(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_purchase_order(obj = Depends(get_purchase_order_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_purchase_order(id: int, data: PurchaseOrderUpdate, db: AsyncSession = Depends(get_db)):
    return await purchase_order_service.update_purchase_order(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_purchase_order(id: int, db: AsyncSession = Depends(get_db)):
    return await purchase_order_service.delete_purchase_order(db, id)
