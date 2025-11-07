from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.expense import Expense
from app.crud.expense import expense_crud


class ExpenseRepository:
    def __init__(self):
        self.crud = expense_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Expense))
        return result.scalars().all()
    
    async def get_by_category(self, db: AsyncSession, category: str):
        """Get expenses by category"""
        result = await db.execute(
            select(Expense).where(Expense.category == category)
        )
        return result.scalars().all()


expense_repository = ExpenseRepository()