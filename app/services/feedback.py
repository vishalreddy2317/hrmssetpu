from app.repositories.feedback import feedback_repository
from app.schemas.feedback import FeedbackCreate, FeedbackUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class FeedbackService:
    def __init__(self):
        self.repo = feedback_repository

    async def create_feedback(self, db: AsyncSession, data: FeedbackCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_feedback(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_feedbacks(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_feedback(self, db: AsyncSession, id: int, data: FeedbackUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_feedback(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

feedback_service = FeedbackService()
