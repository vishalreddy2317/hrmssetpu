from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.role_permission import RolePermission
from app.crud.role_permission import role_permission_crud


class RolePermissionRepository:
    def __init__(self):
        self.crud = role_permission_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(RolePermission))
        return result.scalars().all()


role_permission_repository = RolePermissionRepository()