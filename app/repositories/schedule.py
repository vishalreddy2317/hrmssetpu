from app.crud.schedule import schedule_crud


class ScheduleRepository:
    def __init__(self):
        self.crud = schedule_crud


schedule_repository = ScheduleRepository()