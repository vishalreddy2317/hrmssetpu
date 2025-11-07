from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.payroll import payroll_service
from app.schemas.payroll import PayrollCreate, PayrollUpdate
from app.dependencies.payroll import get_payroll_by_id

router = APIRouter(prefix="/payroll", tags=["Payroll"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_payroll(data: PayrollCreate, db: AsyncSession = Depends(get_db)):
    return await payroll_service.create_payroll(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_payrolls(db: AsyncSession = Depends(get_db)):
    return await payroll_service.list_payrolls(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_payroll(obj = Depends(get_payroll_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_payroll(id: int, data: PayrollUpdate, db: AsyncSession = Depends(get_db)):
    return await payroll_service.update_payroll(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payroll(id: int, db: AsyncSession = Depends(get_db)):
    return await payroll_service.delete_payroll(db, id)
