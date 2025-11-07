from app.models.user_role import UserRole
from app.crud.user_role import user_role_crud
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class UserRoleRepository:
    def __init__(self):
        self.crud = user_role_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(UserRole))
        return result.scalars().all()

user_role_repository = UserRoleRepository()
