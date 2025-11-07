from app.crud.medicine import medicine_crud


class MedicineRepository:
    def __init__(self):
        self.crud = medicine_crud


medicine_repository = MedicineRepository()