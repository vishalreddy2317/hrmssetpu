from app.repositories.chat import chat_repository
from app.schemas.chat import ChatCreate, ChatUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class ChatService:
    def __init__(self):
        self.repo = chat_repository

    async def create_chat(self, db: AsyncSession, data: ChatCreate):
        # Convert Pydantic model to dict
        return await self.repo.crud.create(db, obj_in=data.model_dump())

    async def get_chat(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_chats(self, db: AsyncSession):
        return await self.repo.crud.get_all(db)

    async def update_chat(self, db: AsyncSession, id: int, data: ChatUpdate):
        # First fetch the DB object
        db_obj = await self.repo.crud.get(db, id=id)
        if not db_obj:
            return None  # Or raise an HTTPException

        # Update with only the fields set in the Pydantic model
        return await self.repo.crud.update(db, db_obj=db_obj, obj_in=data.model_dump(exclude_unset=True))

    async def delete_chat(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

# Singleton instance
chat_service = ChatService()
