from app.crud.base import CRUDBase
from app.models.attendance import Attendance
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate

attendance_crud = CRUDBase[Attendance, AttendanceCreate, AttendanceUpdate](Attendance)