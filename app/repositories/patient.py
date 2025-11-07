from app.crud.patient import patient_crud


class PatientRepository:
    def __init__(self):
        self.crud = patient_crud


patient_repository = PatientRepository()