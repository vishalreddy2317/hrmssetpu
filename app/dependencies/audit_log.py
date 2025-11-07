from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.audit_log import audit_log_service

async def get_audit_log_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await audit_log_service.get_audit_log(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AuditLog not found")
    return obj
