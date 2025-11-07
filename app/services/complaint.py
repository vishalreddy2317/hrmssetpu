from app.repositories.complaint import complaint_repository
from app.schemas.complaint import ComplaintCreate, ComplaintUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class ComplaintService:
    def __init__(self):
        self.repo = complaint_repository

    async def create_complaint(self, db: AsyncSession, data: ComplaintCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_complaint(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_complaints(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_complaint(self, db: AsyncSession, id: int, data: ComplaintUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_complaint(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

complaint_service = ComplaintService()
