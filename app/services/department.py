from app.repositories.department import department_repository
from app.schemas.department import DepartmentCreate, DepartmentUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class DepartmentService:
    def __init__(self):
        self.repo = department_repository

    async def create_department(self, db: AsyncSession, data: DepartmentCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_department(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_departments(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_department(self, db: AsyncSession, id: int, data: DepartmentUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_department(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

department_service = DepartmentService()
