from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.payment import payment_service
from app.schemas.payment import PaymentCreate, PaymentUpdate
from app.dependencies.payment import get_payment_by_id

router = APIRouter(prefix="/payment", tags=["Payment"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_payment(data: PaymentCreate, db: AsyncSession = Depends(get_db)):
    return await payment_service.create_payment(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_payments(db: AsyncSession = Depends(get_db)):
    return await payment_service.list_payments(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_payment(obj = Depends(get_payment_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_payment(id: int, data: PaymentUpdate, db: AsyncSession = Depends(get_db)):
    return await payment_service.update_payment(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payment(id: int, db: AsyncSession = Depends(get_db)):
    return await payment_service.delete_payment(db, id)
