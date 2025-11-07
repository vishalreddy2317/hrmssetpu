from app.repositories.transport import transport_repository
from app.schemas.transport import TransportCreate, TransportUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class TransportService:
    def __init__(self):
        self.repo = transport_repository

    async def create_transport(self, db: AsyncSession, data: TransportCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_transport(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_transports(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_transport(self, db: AsyncSession, id: int, data: TransportUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_transport(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

transport_service = TransportService()
