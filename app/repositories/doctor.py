from app.crud.doctor import doctor_crud


class DoctorRepository:
    def __init__(self):
        self.crud = doctor_crud


doctor_repository = DoctorRepository()