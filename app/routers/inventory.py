from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.inventory import inventory_service
from app.schemas.inventory import InventoryCreate, InventoryUpdate
from app.dependencies.inventory import get_inventory_by_id

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_inventory(data: InventoryCreate, db: AsyncSession = Depends(get_db)):
    return await inventory_service.create_inventory(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_inventorys(db: AsyncSession = Depends(get_db)):
    return await inventory_service.list_inventorys(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_inventory(obj = Depends(get_inventory_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_inventory(id: int, data: InventoryUpdate, db: AsyncSession = Depends(get_db)):
    return await inventory_service.update_inventory(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventory(id: int, db: AsyncSession = Depends(get_db)):
    return await inventory_service.delete_inventory(db, id)
