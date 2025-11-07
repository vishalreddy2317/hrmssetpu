from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.billing import billing_service
from app.schemas.billing import BillingCreate, BillingUpdate
from app.dependencies.billing import get_billing_by_id

router = APIRouter(prefix="/billing", tags=["Billing"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_billing(data: BillingCreate, db: AsyncSession = Depends(get_db)):
    return await billing_service.create_billing(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_billings(db: AsyncSession = Depends(get_db)):
    return await billing_service.list_billings(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_billing(obj = Depends(get_billing_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_billing(id: int, data: BillingUpdate, db: AsyncSession = Depends(get_db)):
    return await billing_service.update_billing(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_billing(id: int, db: AsyncSession = Depends(get_db)):
    return await billing_service.delete_billing(db, id)
