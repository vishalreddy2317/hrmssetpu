from app.repositories.message import message_repository
from app.schemas.message import MessageCreate, MessageUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class MessageService:
    def __init__(self):
        self.repo = message_repository

    async def create_message(self, db: AsyncSession, data: MessageCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_message(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_messages(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_message(self, db: AsyncSession, id: int, data: MessageUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_message(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

message_service = MessageService()
