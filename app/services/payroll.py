from app.repositories.payroll import payroll_repository
from app.schemas.payroll import PayrollCreate, PayrollUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class PayrollService:
    def __init__(self):
        self.repo = payroll_repository

    async def create_payroll(self, db: AsyncSession, data: PayrollCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_payroll(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_payrolls(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_payroll(self, db: AsyncSession, id: int, data: PayrollUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_payroll(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

payroll_service = PayrollService()
