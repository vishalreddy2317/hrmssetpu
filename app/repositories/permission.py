from app.models.permission import Permission
from app.crud.permission import permission_crud
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class PermissionRepository:
    def __init__(self):
        self.crud = permission_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Permission))
        return result.scalars().all()

permission_repository = PermissionRepository()
