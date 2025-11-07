from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.audit_log import AuditLog
from app.crud.audit_log import audit_log_crud


class AuditLogRepository:
    def __init__(self):
        self.crud = audit_log_crud

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(AuditLog))
        return result.scalars().all()


audit_log_repository = AuditLogRepository()