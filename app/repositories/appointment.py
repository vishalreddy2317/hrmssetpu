from app.crud.appointment import appointment_crud


class AppointmentRepository:
    def __init__(self):
        self.crud = appointment_crud


appointment_repository = AppointmentRepository()