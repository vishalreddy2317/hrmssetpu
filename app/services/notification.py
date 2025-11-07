from app.repositories.notification import notification_repository
from app.schemas.notification import NotificationCreate, NotificationUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class NotificationService:
    def __init__(self):
        self.repo = notification_repository

    async def create_notification(self, db: AsyncSession, data: NotificationCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_notification(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_notifications(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_notification(self, db: AsyncSession, id: int, data: NotificationUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_notification(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

notification_service = NotificationService()
