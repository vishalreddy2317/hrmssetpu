from app.crud.prescription import prescription_crud


class PrescriptionRepository:
    def __init__(self):
        self.crud = prescription_crud


prescription_repository = PrescriptionRepository()