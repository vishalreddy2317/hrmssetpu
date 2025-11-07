from app.repositories.procedure import procedure_repository
from app.schemas.procedure import ProcedureCreate, ProcedureUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class ProcedureService:
    def __init__(self):
        self.repo = procedure_repository

    async def create_procedure(self, db: AsyncSession, data: ProcedureCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_procedure(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_procedures(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_procedure(self, db: AsyncSession, id: int, data: ProcedureUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_procedure(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

procedure_service = ProcedureService()
