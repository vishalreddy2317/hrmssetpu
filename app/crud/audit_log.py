from app.crud.base import CRUDBase
from app.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogCreate, AuditLogUpdate

audit_log_crud = CRUDBase[AuditLog, AuditLogCreate, AuditLogUpdate](AuditLog)