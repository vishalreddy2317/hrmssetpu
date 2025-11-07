from app.crud.shift import shift_crud


class ShiftRepository:
    def __init__(self):
        self.crud = shift_crud


shift_repository = ShiftRepository()