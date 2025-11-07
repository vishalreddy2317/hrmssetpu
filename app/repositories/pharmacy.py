from app.crud.pharmacy import pharmacy_crud


class PharmacyRepository:
    def __init__(self):
        self.crud = pharmacy_crud


pharmacy_repository = PharmacyRepository()