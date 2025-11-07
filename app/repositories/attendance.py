from app.crud.attendance import attendance_crud


class AttendanceRepository:
    def __init__(self):
        self.crud = attendance_crud


attendance_repository = AttendanceRepository()