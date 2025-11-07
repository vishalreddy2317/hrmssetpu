from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.payroll import payroll_service

async def get_payroll_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await payroll_service.get_payroll(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payroll not found")
    return obj
