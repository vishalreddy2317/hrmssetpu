from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.expense import expense_service


async def get_expense_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await expense_service.get_expense(db, id=id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Expense not found"
        )
    return obj