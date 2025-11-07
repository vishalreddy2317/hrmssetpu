from app.crud.base import CRUDBase
from app.models.activity_log import ActivityLog
from app.schemas.activity_log import ActivityLogCreate, ActivityLogUpdate

activity_log_crud = CRUDBase[ActivityLog, ActivityLogCreate, ActivityLogUpdate](ActivityLog)