from app.repositories.role_permission import role_permission_repository
from app.schemas.role_permission import RolePermissionCreate, RolePermissionUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class RolePermissionService:
    def __init__(self):
        self.repo = role_permission_repository

    async def create_role_permission(self, db: AsyncSession, data: RolePermissionCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_role_permission(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_role_permissions(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_role_permission(self, db: AsyncSession, id: int, data: RolePermissionUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_role_permission(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

role_permission_service = RolePermissionService()
