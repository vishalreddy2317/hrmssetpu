from app.crud.nurse import nurse_crud


class NurseRepository:
    def __init__(self):
        self.crud = nurse_crud


nurse_repository = NurseRepository()