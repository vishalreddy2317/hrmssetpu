from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.audit_log import audit_log_service
from app.schemas.audit_log import AuditLogCreate, AuditLogUpdate
from app.dependencies.audit_log import get_audit_log_by_id

router = APIRouter(prefix="/audit_log", tags=["AuditLog"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_audit_log(data: AuditLogCreate, db: AsyncSession = Depends(get_db)):
    return await audit_log_service.create_audit_log(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_audit_logs(db: AsyncSession = Depends(get_db)):
    return await audit_log_service.list_audit_logs(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_audit_log(obj = Depends(get_audit_log_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_audit_log(id: int, data: AuditLogUpdate, db: AsyncSession = Depends(get_db)):
    return await audit_log_service.update_audit_log(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_audit_log(id: int, db: AsyncSession = Depends(get_db)):
    return await audit_log_service.delete_audit_log(db, id)
