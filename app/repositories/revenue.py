from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.revenue import Revenue
from app.crud.revenue import revenue_crud


class RevenueRepository:
    def __init__(self):
        self.crud = revenue_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Revenue))
        return result.scalars().all()
    
    async def get_by_source(self, db: AsyncSession, source: str):
        """Get revenue by source"""
        result = await db.execute(
            select(Revenue).where(Revenue.source == source)
        )
        return result.scalars().all()


revenue_repository = RevenueRepository()