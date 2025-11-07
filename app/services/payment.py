from app.repositories.payment import payment_repository
from app.schemas.payment import PaymentCreate, PaymentUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class PaymentService:
    def __init__(self):
        self.repo = payment_repository

    async def create_payment(self, db: AsyncSession, data: PaymentCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_payment(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_payments(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_payment(self, db: AsyncSession, id: int, data: PaymentUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_payment(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

payment_service = PaymentService()
