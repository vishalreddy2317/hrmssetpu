from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.branch import Branch
from app.crud.branch import branch_crud


class BranchRepository:
    def __init__(self):
        self.crud = branch_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Branch))
        return result.scalars().all()
    
    async def get_by_hospital_id(self, db: AsyncSession, hospital_id: int):
        """Get all branches for a hospital"""
        result = await db.execute(
            select(Branch).where(Branch.hospital_id == hospital_id)
        )
        return result.scalars().all()
    
    async def get_active(self, db: AsyncSession):
        """Get all active branches"""
        result = await db.execute(
            select(Branch).where(Branch.is_active == True)
        )
        return result.scalars().all()


branch_repository = BranchRepository()