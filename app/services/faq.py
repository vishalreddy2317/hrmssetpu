from app.repositories.faq import faq_repository
from app.schemas.faq import  FAQCreate, FAQUpdate
from sqlalchemy.ext.asyncio import AsyncSession

async def get_all(self, db: AsyncSession):
    raise NotImplementedError

class FaqService:
    def __init__(self):
        self.repo = faq_repository

    async def create_faq(self, db: AsyncSession, data:  FAQCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_faq(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_faqs(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_faq(self, db: AsyncSession, id: int, data: FAQUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_faq(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

faq_service = FaqService()
