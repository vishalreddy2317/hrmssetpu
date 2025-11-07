from app.crud.base import CRUDBase
from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate

schedule_crud = CRUDBase[Schedule, ScheduleCreate, ScheduleUpdate](Schedule)