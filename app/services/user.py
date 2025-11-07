from app.repositories.user import user_repository
from app.schemas.user import UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class UserService:
    def __init__(self):
        self.repo = user_repository

    async def create_user(self, db: AsyncSession, data: UserCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_user(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_users(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_user(self, db: AsyncSession, id: int, data: UserUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_user(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

user_service = UserService()
