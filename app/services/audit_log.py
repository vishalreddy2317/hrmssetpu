from app.repositories.audit_log import audit_log_repository
from app.schemas.audit_log import AuditLogCreate, AuditLogUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class AuditLogService:
    def __init__(self):
        self.repo = audit_log_repository

    async def create_audit_log(self, db: AsyncSession, data: AuditLogCreate):
        return await self.repo.crud.create(db, obj_in=data)

    async def get_audit_log(self, db: AsyncSession, id: int):
        return await self.repo.crud.get(db, id=id)

    async def list_audit_logs(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update_audit_log(self, db: AsyncSession, id: int, data: AuditLogUpdate):
        return await self.repo.crud.update(db, id=id, obj_in=data)

    async def delete_audit_log(self, db: AsyncSession, id: int):
        return await self.repo.crud.remove(db, id=id)

audit_log_service = AuditLogService()
