from app.crud.leave import leave_crud


class LeaveRepository:
    def __init__(self):
        self.crud = leave_crud


leave_repository = LeaveRepository()