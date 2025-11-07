from app.crud.diagnosis import diagnosis_crud


class DiagnosisRepository:
    def __init__(self):
        self.crud = diagnosis_crud


diagnosis_repository = DiagnosisRepository()