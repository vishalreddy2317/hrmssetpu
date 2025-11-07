from app.repositories.role import role_repository
from app.schemas.role import RoleCreate, RoleUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class RoleService:
    def __init__(self):
        self.repo = role_repository

    async def create_role(self, db: AsyncSession, data: RoleCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_role(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_roles(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_role(self, db: AsyncSession, id: int, data: RoleUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_role(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

role_service = RoleService()
