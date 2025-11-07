from app.crud.insurance import insurance_crud


class InsuranceRepository:
    def __init__(self):
        self.crud = insurance_crud


insurance_repository = InsuranceRepository()